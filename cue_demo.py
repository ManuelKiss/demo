# 原始代码
def get_user_info(username):
    """获取用户信息"""
    print(f"正在查询用户: {username}")
    
    # 从数据库获取数据
    user_data = db.query(username)
    
    if user_data:
        return {
            "name": username,
            "email": user_data.email,
            "status": user_data.status
        }
    return None

# 调用函数
result = get_user_info(username="张三") 
print(result)