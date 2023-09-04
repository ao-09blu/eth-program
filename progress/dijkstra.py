import sys
import heapq

def dijkstra(graph, start):
    #初期化
    n = len(graph)
    visited = [False] * n
    distance = [sys.maxsize] * n
    distance[start] = 0
    #u=start
    previous = [None] * n
    #ダイクストラ法
    for i in range(n):
        #未処理の中で最小の距離を持つ頂点を探す
        min_distance = sys.maxsize

        for j in range(n):
            if not visited[j] and distance[j] < min_distance: #未到達かつ最小の距離を見つける
                min_distance = distance[j]
                u = j
                
        #訪問済みにする
        visited[u] = True

        #uから到達可能な頂点の距離を更新する
        for v in range(n):
            if not visited[v] and graph[u][v] != 0:
                new_distance = distance[u] + graph[u][v]
                if new_distance < distance[v]:
                    distance[v] = new_distance
                    previous[v] = u
            
    # 最短経路の頂点リストを作成する
    path = []
    for i in range(n):
        path.append([])
        if i == start:
            continue
        if previous[i] is not None:
            node = i
            while node is not None:
                path[i].insert(0, node)
                node = previous[node]
        else:
            path.append(None)
    # 最短経路上の頂点リストを返す
    return path



def dijkstra_list(graph, start):
    # 初期化
    n = len(graph)
    visited = [False] * n
    distance = [sys.maxsize] * n
    distance[start] = 0
    pq = [(0, start)]

    # ダイクストラ法
    while pq:
        # 未処理の中で最小の距離を持つ頂点を取り出す
        dist, u = heapq.heappop(pq)
        if visited[u]:
            continue

        # 訪問済みにする
        visited[u] = True

        # uから到達可能な頂点の距離を更新する
        for v, weight in graph[u]:
            if not visited[v]:
                new_distance = distance[u] + weight
                if new_distance < distance[v]:
                    distance[v] = new_distance
                    heapq.heappush(pq, (new_distance, v))

    return distance

graph =[ [0, 2, 4, 0, 0],
    [2, 0, 1, 4, 0],
    [4, 1, 0, 1, 3],
    [0, 4, 1, 0, 1],
    [0, 0, 3, 1, 0]]

start = 1

for i in range(5):
    print("Startnode: Router", i)
    distance = dijkstra(graph, i)
    print(distance)


"""
graph_list =[
    [(1, 2), (2, 4)],
    [(0, 2), (2, 1), (3, 4)],
    [(0, 4), (1, 1), (3, 1), (4, 3)],
    [(1, 4), (2, 1), (4, 1)],
    [(2, 3), (3, 1)]
]
start = 3
distance_list = dijkstra_list(graph_list, start)
print(distance_list)
"""
