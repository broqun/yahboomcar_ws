#include "arm_kin/fk_ik_kin.h"
#include <cmath>

bool arm_getFK(const char *urdf_file, vector<double> &joints, vector<double> &currentPos) {
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

bool arm_getIK(const char *urdf_file,
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