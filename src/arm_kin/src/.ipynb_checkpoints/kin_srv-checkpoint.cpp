#include "rclcpp/rclcpp.hpp"
#include "arm_interface/srv/arm_kinemarics.hpp"
//not ros
#include <kdl/chain.hpp>
#include <kdl/tree.hpp>
#include <kdl/segment.hpp>
#include <kdl/frames_io.hpp>
#include <kdl/chainiksolverpos_lma.hpp>
#include <kdl/chainfksolverpos_recursive.hpp>
#include <kdl_parser/kdl_parser.hpp>
#include <iostream>
#include <kdl/chain.hpp>
#include <kdl/chainfksolver.hpp>
#include <kdl/tree.hpp>
#include <kdl_parser/kdl_parser.hpp>
#include <kdl_parser/kdl_parser.hpp>


using namespace KDL;
using namespace std;
// 弧度转角度
const float RA2DE = 180.0f / M_PI;
// 角度转弧度
const float DE2RA = M_PI / 180.0f;
const char *urdf_file = "/root/yahboomcar_ws/src/yahboom_M3Pro_description/urdf/M3Pro.urdf";
int a = 0;

/**
 * 正向运动学计算 根据旋转关节角获取当前位姿
 * @param urdf_file 模型文件路径
 * @param joints    当前关节角度
 * @param cartpos   当前末端位姿
 */
bool arm_getFK(const string &urdf_file, vector<double> &joints, vector<double> &currentPos) {
    Tree my_tree;
    // 读取机械臂模型文件
    kdl_parser::treeFromFile(urdf_file, my_tree);
    Chain chain;
    // 获得机械臂运动链结构信息
    bool exit_value = my_tree.getChain("base_link", "Gripping", chain);
    // 判断获取机械臂信息情况
    if (!exit_value) {
        //cout << "There was no valid KDL chain found!" << endl;
        return false;
    }
    // 实现了一种递推位置运动学算法，用于计算一般运动链从关节空间到笛卡尔空间的位置变换。
    ChainFkSolverPos_recursive fksolver = ChainFkSolverPos_recursive(chain);
    // 获得连关节数量
    unsigned int nj = chain.getNrOfJoints();
    cout<<nj<<endl;
    // 获得所需当前关节信息类型
    JntArray jointpositions(nj);
    for (int j = 0; j < nj; ++j) jointpositions(j) = joints.at(j);
    // 定义正解结果容器
    Frame cartpos;
    // 正解计算
    bool kinematics_status = fksolver.JntToCart(jointpositions, cartpos);
    // 将正解结果存入currentPos传输出去
    double r, p, y; // 绕x,y,z轴转动
    cartpos.M.GetRPY(r, p, y);
    currentPos.push_back(cartpos.p.x());
    currentPos.push_back(cartpos.p.y());
    currentPos.push_back(cartpos.p.z());
    currentPos.push_back(r);
    currentPos.push_back(p);
    currentPos.push_back(y);
    // 判断正解状态
    if (kinematics_status >= 0) return true;
    else return false;
}

/**
 * 逆运动学计算 获取到到目标点各关节需要转动的角度
 * @param urdf_file  模型文件路径
 * @param initjoints 当前关节角度
 * @param targetXYZ  目标位置
 * @param targetRPY  目标姿态
 * @param outjoints  目标点关节角度
 */
bool arm_getIK(const string &urdf_file,
               vector<double> &targetXYZ,
               vector<double> &targetRPY,
               vector<double> &outjoints) {
    // 机械臂初始角度
    double initjoints[]{0, 0, 0, 0, 0};
    Tree my_tree;
    // 读取机械臂模型文件
    kdl_parser::treeFromFile(urdf_file, my_tree);
    Chain chain;
    // 获得机械臂运动链结构信息
    bool exit_value = my_tree.getChain("base_link", "Gripping", chain);
    // 判断获取机械臂信息情况
    if (!exit_value) {
        //cout << "There was no valid KDL chain found!" << endl;
        return false;
    }
    // 权重矩阵
    double eps = 1E-5;
    // 指定最大迭代次数。
    int maxiter = 500;
    // 指定当计算出的关节角度增量小于eps关节时，算法必须停止。
    double eps_joints = 1E-15;
    // 构造一个lma解算器。
    ChainIkSolverPos_LMA iksolver = ChainIkSolverPos_LMA(chain, eps, maxiter, eps_joints);
    // 获得连关节数量
    unsigned int nj = chain.getNrOfJoints();
    // 获得所需当前关节信息类型
    JntArray jointGuesspositions(nj);
    for (int i = 0; i < nj; ++i) jointGuesspositions(i) = initjoints[i];
    float cy = cos(targetRPY.at(2));
    float sy = sin(targetRPY.at(2));
    float cp = cos(targetRPY.at(1));
    float sp = sin(targetRPY.at(1));
    float cr = cos(targetRPY.at(0));
    float sr = sin(targetRPY.at(0));
    double rot0 = cy * cp;
    double rot1 = cy * sp * sr - sy * cr;
    double rot2 = cy * sp * cr + sy * sr;
    double rot3 = sy * cp;
    double rot4 = sy * sp * sr + cy * cr;
    double rot5 = sy * sp * cr - cy * sr;
    double rot6 = -sp;
    double rot7 = cp * sr;
    double rot8 = cp * cr;
    // 获得旋转矩阵
    //Rotation rot = KDL::Rotation::Identity();
    Rotation rot = Rotation(rot0, rot1, rot2, rot3, rot4, rot5, rot6, rot7, rot8);
     cout << "+-+-+-+" << endl;
    cout << rot << endl;
    // 获得平移矩阵
    Vector vector = Vector(targetXYZ.at(0), targetXYZ.at(1), targetXYZ.at(2));
    // 合成旋转平移矩阵
    Frame cartpos = Frame(rot, vector);
    // 定义反解结果容器
    JntArray jointpositions(nj);
    // 计算逆位置运动学。
    bool kinematics_status = iksolver.CartToJnt(jointGuesspositions, cartpos, jointpositions);
    // 判断反解状态
    if (kinematics_status >= 0) {
        for (int i = 0; i < nj; i++) outjoints.push_back((double) jointpositions(i));
        return true;
    } else return false;
}

void handle_service(
  const std::shared_ptr<arm_interface::srv::ArmKinemarics::Request> request,
  std::shared_ptr<arm_interface::srv::ArmKinemarics::Response> response)
{
  cout<<"-----------------"<<endl;
  cout<<request->kin_name<<endl;
  //RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "I got it.");
  //RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "kin name is %f.",request->tar_z);
      if (request->kin_name == "fk") {
        double joints[]{request->cur_joint1, request->cur_joint2, request->cur_joint3, request->cur_joint4,
                        request->cur_joint5,request->cur_joint6};
        // 定义目标关节角容器
        vector<double> initjoints;
        // 定义位姿容器
        vector<double> initpos;
        // 目标关节角度单位转换,由角度转换成弧度
        for (int i = 0; i < 6; ++i) initjoints.push_back((joints[i] - 90) * DE2RA);
        arm_getFK(urdf_file, initjoints, initpos);
        response->x = initpos.at(0);
        response->y = initpos.at(1);
        response->z = initpos.at(2);
        response->roll = initpos.at(3);
        response->pitch = initpos.at(4);
        response->yaw = initpos.at(5);
        cout<<"-----------------"<<endl;
    }
    
    if (request->kin_name == "ik") {
        // 夹抓长度
        double tool_param = 0.12;
        // 抓取的位姿
        double Roll = request->roll ;
        double Pitch = request->pitch;
        double Yaw = request->yaw ;
        double x=request->tar_x;
        double y=request->tar_y;
        double z=request->tar_z;
        // 末端位置(单位: m)
        double xyz[]{x, y, z};
        cout << x << y << z << endl;
        // 末端姿态(单位: 弧度)
        //double rpy[]{Roll * DE2RA, Pitch * DE2RA, Yaw * DE2RA};
    	double rpy[]{Roll , Pitch, Yaw };
        // 创建输出角度容器
        vector<double> outjoints;
        // 创建末端位置容器
        vector<double> targetXYZ;
        // 创建末端姿态容器
        vector<double> targetRPY;
        for (int k = 0; k < 3; ++k) targetXYZ.push_back(xyz[k]);
        for (int l = 0; l < 3; ++l) targetRPY.push_back(rpy[l]);
        // 反解求到达目标点的各关节角度
        arm_getIK(urdf_file, targetXYZ, targetRPY, outjoints);
        // 打印反解结果
        for (int i = 0; i < 5; i++) cout << (outjoints.at(i) * RA2DE) + 90 << ",";
        cout << endl;
        a++;
        response->joint1 = (outjoints.at(0) * RA2DE) + 90;
        response->joint2 = (outjoints.at(1) * RA2DE) + 90;
        response->joint3 = (outjoints.at(2) * RA2DE) + 90;
        response->joint4 = (outjoints.at(3) * RA2DE) + 90;
        response->joint5 = (outjoints.at(4) * RA2DE) + 90;
        cout<<"-----------------"<<endl;
    }
  
  

}

int main(int argc,char **argv)
{
	rclcpp::init(argc, argv);
	auto node = rclcpp::Node::make_shared("kinemarics_arm");
	auto service = node->create_service<arm_interface::srv::ArmKinemarics>("get_kinemarics", handle_service);
	rclcpp::spin(node);
	rclcpp::shutdown();
	return 0;	
}

