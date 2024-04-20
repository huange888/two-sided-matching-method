def gale_shapley_matching(transfer_stations, demand_points, max_capacity):
    # 初始化匹配状态
    matched_transfer_stations = [False] * len(transfer_stations)
    matched_demand_points = [False] * len(demand_points)

    # 偏好列表，需求点到中转站的偏好
    preferences = [
        # 需求点 i 偏好的中转站列表
        [1, 2, 0],  # 需求点 0 的偏好
        [0, 2, 1],  # 需求点 1 的偏好
        [0, 1, 2],  # 需求点 2 的偏好
    ]

    while not all(matched_demand_points):
        for demand_point in range(len(demand_points)):
            if not matched_demand_points[demand_point]:
                # 获取需求点的偏好列表
                pref_list = preferences[demand_point]
                # 找到当前需求点最满意的中转站（未匹配的）
                preferred_station = None
                for station in pref_list:
                    if not matched_transfer_stations[station]:
                        preferred_station = station
                        break

                if preferred_station is not None:
                    # 如果中转站未匹配，则进行匹配
                    matched_demand_points[demand_point] = True
                    matched_transfer_stations[preferred_station] = True
                    # 检查中转站是否达到最大服务能力
                    if any(matched_transfer_stations[i] for i in
                           range(preferred_station, len(transfer_stations), preferred_station + 1)):
                        # 如果中转站已满，则取消匹配
                        matched_demand_points[demand_point] = False
                        break

    return matched_demand_points


# 示例数据
transfer_stations = ["A", "B", "C"]
demand_points = ["D1", "D2", "D3"]
max_capacity = 1  # 假设每个中转站的最大服务能力为1

# 执行匹配
matched = gale_shapley_matching(transfer_stations, demand_points, max_capacity)
print("匹配结果:", matched)