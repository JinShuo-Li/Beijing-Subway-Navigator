import copy


class Matrix:
    def __init__(self, data=None, dim=None, init_value=0):
        if data == None and dim == None:
            raise ValueError("1-1: Lack enough variables")
        if data is not None:
            if not isinstance(data, list):
                raise TypeError("1-2: The data should be a nested list")
            else:
                for i in range(len(data)):
                    if i == 0:
                        if not isinstance(data[i], list):
                            raise TypeError(
                                "1-3: All the elements in 'data' should be a list"
                            )
                        else:
                            continue
                    else:
                        if (not isinstance(data[i], list)) or (
                            len(data[i]) != len(data[i - 1])
                        ):
                            raise TypeError(
                                "1-4: All the elements in 'data' should be a list and they must have the same lenth to be a matrix"
                            )
                        else:
                            continue
            if len(data) == 0:
                self.data = []
                self.dim = (0, 0)
                self.init_value = init_value
            else:
                row_num = len(data)
                col_num = len(data[0])
                dim = (row_num, col_num)
        else:
            if not isinstance(dim, tuple):
                raise TypeError("1-5: The variable 'dim' should be a tuple")
            if len(dim) != 2:
                raise ValueError("1-6: The tuple 'dim' should contains two elements")
            m, n = dim
            if not (isinstance(m, int) and isinstance(n, int)):
                raise TypeError("1-7: The elements in 'dim' should be integers")
            data = [[init_value for _ in range(n)] for _ in range(m)]
        self.data = data
        self.dim = dim
        self.init_value = init_value

    def T(self):
        if not isinstance(self, Matrix):
            raise TypeError("5-1: Only Matrix objects can be transposed")
        res = []
        for i in range(len(self.data[0])):
            new_row = []
            for j in range(len(self.data)):
                new_row.append(self.data[j][i])
            res.append(new_row)
        return Matrix(res)

    def __pow__(self, n):
        if not isinstance(n, int):
            raise TypeError("11-1: Exponent must be an integer")
        if not isinstance(self, Matrix):
            raise TypeError("11-2: Only Matrix objects can be exponentiated")
        if len(self.data) == 0 or len(self.data[0]) == 0:
            raise ValueError("11-3: We do not accept empty matrix and list")
        if len(self.data) != len(self.data[0]):
            return ValueError("11-4: Only square matrix can be exponentiated")
        res = Matrix(data=self.data)
        for _ in range(n - 1):
            res = res * self
            res = Matrix(data=res.data)
        return res

    def __add__(self, other):
        if (not isinstance(self, Matrix)) or (not isinstance(other, Matrix)):
            raise TypeError("12-1: Only Matrix objects can be added")
        res = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(self.data[0])):
                row.append(self.data[i][j] + other.data[i][j])
            res.append(row)
        return Matrix(data=res)

    def __mul__(self, other):
        if not (isinstance(self, Matrix) and isinstance(other, Matrix)):
            raise TypeError("4-1: Self and other should be Matrix obects")
        new_self = self.data
        new_other = (other.T()).data
        width = len(new_self[0])
        res = []
        for i in range(len(new_self)):
            new_row = []
            for j in range(len(new_other)):
                new_ele = 0
                for k in range(width):
                    new_ele += new_self[i][k] * new_other[j][k]
                new_row.append(new_ele)
            res.append(new_row)
        return Matrix(data=res)


class Graph:
    def __init__(self, data=[]):
        self.data = data

    def get_neighbors(self, vertex):
        neighbors = []
        for i in range(len(self.data[vertex])):
            if self.data[vertex][i] != 0:
                neighbors.append(i)
        return neighbors

    def get_degree(self, vertex):
        out_degree = 0
        in_degree = 0
        vertices_count = len(self.data)
        for i in range(vertices_count):
            if self.data[vertex][i] != 0:
                out_degree += 1
        for j in range(vertices_count):
            if self.data[j][vertex] != 0:
                in_degree += 1
        return (out_degree, in_degree)

    def add_edge(self, start, end, weight=1):
        self.data[start][end] = weight

    def remove_edge(self, start, end):
        self.data[start][end] = 0

    def count_edges(self):
        count = 0
        for i in range(len(self.data)):
            for j in range(len(self.data)):
                if self.data[i][j] != 0:
                    count += 1
        return count

    def is_complete(self):
        vertices_count = len(self.data)
        for i in range(vertices_count):
            for j in range(vertices_count):
                if i != j:
                    if self.data[i][j] == 0:
                        return False
        return True

    def find_shortest_path_CPX(self, start, end):
        vertices_count = len(self.data)
        if start == end:
            return [start]
        adj_matrix = Matrix(copy.deepcopy(self.data))
        matrices = [Matrix(copy.deepcopy(self.data))]
        found = False
        limit = 10

        for i in range(limit):
            if matrices[-1].data[start][end] != 0:
                found = True
                break
            matrices.append(matrices[-1] * adj_matrix)

        if not found:
            return None
        return ["Path exists (Computed via Matrix Power)"]

    def find_shortest_path_BFS(self, start, end):
        vertices_count = len(self.data)
        queue = [start]
        mat = self.data
        memory = {start: None}
        found = False
        idx = 0
        while idx < len(queue):
            curr = queue[idx]
            idx += 1
            if curr == end:
                found = True
                break
            for i in range(vertices_count):
                if mat[curr][i] != 0 and i not in memory:
                    memory[i] = curr
                    queue.append(i)
                    if i == end:
                        found = True
                        break
            if found:
                break
        if not found:
            return None
        path = []
        index = end
        while index is not None:
            path.append(index)
            index = memory[index]
        return path[::-1]

    def find_path_DFS(self, start, end):
        vertices_count = len(self.data)
        stack = [start]
        mat = self.data
        memory = {start: None}
        found = False
        while len(stack) > 0:
            curr = stack.pop()
            if curr == end:
                found = True
                break
            for i in range(vertices_count):
                if mat[curr][i] != 0 and i not in memory:
                    memory[i] = curr
                    stack.append(i)
        if not found:
            return None
        path = []
        curr_node = end
        while curr_node is not None:
            path.append(curr_node)
            curr_node = memory[curr_node]
        return path[::-1]

    def find_shortest_path_weight(self, start, end):
        vertices_count = len(self.data)
        distances = {i: float("inf") for i in range(vertices_count)}
        distances[start] = 0
        visited = [False] * vertices_count
        parent = {start: None}
        for _ in range(vertices_count):
            min_dist = float("inf")
            curr = -1
            for i in range(vertices_count):
                if not visited[i] and distances[i] < min_dist:
                    min_dist = distances[i]
                    curr = i
            if curr == -1 or distances[curr] == float("inf"):
                break
            if curr == end:
                break
            visited[curr] = True
            for i in range(vertices_count):
                weight = self.data[curr][i]
                if weight > 0 and not visited[i]:
                    new_dist = distances[curr] + weight
                    if new_dist < distances[i]:
                        distances[i] = new_dist
                        parent[i] = curr
        if end not in parent:
            return None, float("inf")
        path = []
        curr_node = end
        while curr_node is not None:
            path.append(curr_node)
            curr_node = parent[curr_node]
        return path[::-1], distances[end]

    def minimum_spanning_tree_prim(self, weights):
        n = len(weights)
        INF = float("inf")
        key = [INF] * n
        parent = [None] * n
        mst_set = [False] * n
        key[0] = 0
        parent[0] = -1
        for _ in range(n):
            min_val = INF
            u = -1
            for v in range(n):
                if not mst_set[v] and key[v] < min_val:
                    min_val = key[v]
                    u = v
            if u == -1:
                break
            mst_set[u] = True
            for v in range(n):
                w = weights[u][v]
                if w > 0 and not mst_set[v] and w < key[v]:
                    key[v] = w
                    parent[v] = u
        mst_matrix = [[0] * n for _ in range(n)]
        total_weight = 0
        for i in range(1, n):
            if parent[i] is not None:
                u, v = parent[i], i
                weight = weights[u][v]
                mst_matrix[u][v] = weight
                mst_matrix[v][u] = weight
                total_weight += weight
        return mst_matrix, total_weight

    def connectness(self):
        start_node = 0
        q = [start_node]
        visited = {start_node}
        while q:
            u = q.pop(0)
            for v in range(len(self.data)):
                if self.data[u][v] > 0 and v not in visited:
                    visited.add(v)
                    q.append(v)
        return len(visited) == len(self.data)

    def connect_components(self):
        mat = self.data
        vertices_count = len(mat)
        visited = [False] * vertices_count
        res = []
        for index in range(vertices_count):
            if not visited[index]:
                component = []
                q = [index]
                visited[index] = True
                while q:
                    u = q.pop(0)
                    component.append(u)
                    for v in range(vertices_count):
                        if mat[u][v] > 0 and not visited[v]:
                            visited[v] = True
                            q.append(v)
                res.append(component)
        return res

    def is_bipartite_BFS(self):
        mat = self.data
        vertices_count = len(mat)
        color = {}
        for start in range(vertices_count):
            if start not in color:
                color[start] = 0
                queue = [start]
                while queue:
                    u = queue.pop(0)
                    for v in range(vertices_count):
                        if mat[u][v] != 0:
                            if v not in color:
                                color[v] = 1 - color[u]
                                queue.append(v)
                            elif color[v] == color[u]:
                                return False
        return True


subway_data_source = {
    "1号线": "苹果园-3-古城-2-八角游乐园-2-八宝山-2-玉泉路-2-五棵松-2-万寿路-2-公主坟-2-军事博物馆-2-木樨地-2-南礼士路-2-复兴门-2-西单-2-天安门西-2-天安门东-2-王府井-2-东单-2-建国门-2-永安里-2-国贸-2-大望路-2-四惠-2-四惠东-3-高碑店-2-传媒大学-2-双桥-2-管庄-2-八里桥-3-通州北苑-2-果园-2-九棵树-2-梨园-2-临河里-2-土桥-2-花庄-2-环球度假区",
    "2号线": "西直门-2-积水潭-2-鼓楼大街-2-安定门-2-雍和宫-2-东直门-2-东四十条-2-朝阳门-2-建国门-2-北京站-2-崇文门-2-前门-2-和平门-2-宣武门-2-长椿街-2-复兴门-2-阜成门-2-车公庄-2-西直门",
    "3号线": "东四十条-2-工人体育场-2-团结湖-2-朝阳公园-2-石佛营-2-朝阳站-3-姚家园-2-东坝南-2-东坝北-2-东风-3-体育中心",
    "4号线": "安河桥北-2-北宫门-2-西苑-2-圆明园-2-北京大学东门-2-中关村-2-海淀黄庄-2-人民大学-2-魏公村-2-国家图书馆-2-动物园-2-西直门-2-新街口-2-平安里-2-西四-2-灵境胡同-2-西单-2-宣武门-2-菜市口-2-陶然亭-2-北京南站-2-马家堡-2-角门西-2-公益西桥-3-新宫-3-西红门-3-高米店北-2-高米店南-2-枣园-2-清源路-2-黄村西大街-2-黄村火车站-2-义和庄-3-生物医药基地-3-天宫院",
    "5号线": "天通苑北-2-天通苑-2-天通苑南-3-立水桥-3-立水桥南-2-北苑路北-2-大屯路东-2-惠新西街北口-2-惠新西街南口-2-和平西桥-2-和平里北街-2-雍和宫-2-北新桥-2-张自忠路-2-东四-2-灯市口-2-东单-2-崇文门-2-磁器口-2-天坛东门-2-蒲黄榆-2-刘家窑-2-宋家庄",
    "6号线": "金安桥-2-苹果园-2-杨庄-2-西黄村-3-廖公庄-2-田村-2-海淀五路居-2-慈寿寺-2-花园桥-2-白石桥南-2-车公庄西-2-车公庄-2-平安里-2-北海北-2-南锣鼓巷-2-东四-2-朝阳门-2-东大桥-2-呼家楼-2-金台路-2-十里堡-2-青年路-3-褡裢坡-3-黄渠-2-常营-2-草房-3-物资学院路-3-通州北关-2-通运门-2-北运河西-2-北运河东-2-郝家府-2-东夏园-2-潞城",
    "7号线": "北京西站-2-湾子-2-达官营-2-广安门内-2-菜市口-2-虎坊桥-2-珠市口-2-桥湾-2-磁器口-2-广渠门内-2-广渠门外-2-双井-2-九龙山-2-大郊亭-2-百子湾-2-化工-2-南楼梓庄-2-欢乐谷景区-3-垡头-2-双合-2-焦化厂-3-黄厂-3-郎辛庄-2-黑庄户-3-万盛西-2-万盛东-2-群芳-2-高楼金-2-花庄-2-环球度假区",
    "8号线": "朱辛庄-3-育知路-2-平西府-3-回龙观东大街-2-霍营-2-育新-2-西小口-2-永泰庄-2-林萃桥-3-森林公园南门-2-奥林匹克公园-2-奥体中心-2-北土城-2-安华桥-2-安德里北街-2-鼓楼大街-2-什刹海-2-南锣鼓巷-2-中国美术馆-2-金鱼胡同-2-王府井-2-前门-3-珠市口-2-天桥-2-永定门外-2-木樨园-2-海户屯-2-大红门-2-大红门南-2-和义-2-东高地-2-火箭万源-2-五福堂-2-德茂-2-瀛海",
    "9号线": "国家图书馆-2-白石桥南-2-白堆子-2-军事博物馆-2-北京西站-2-六里桥东-2-六里桥-2-七里庄-2-丰台东大街-2-丰台南路-2-科怡路-2-丰台科技园-2-郭公庄",
    "10号线": "巴沟-2-苏州街-2-海淀黄庄-2-知春里-2-知春路-2-西土城-2-牡丹园-2-健德门-2-北土城-2-安贞门-2-惠新西街南口-2-芍药居-2-太阳宫-2-三元桥-2-亮马桥-2-农业展览馆-2-团结湖-2-呼家楼-2-金台夕照-2-国贸-2-双井-2-劲松-2-潘家园-2-十里河-2-分钟寺-3-成寿寺-2-宋家庄-2-石榴庄-2-大红门-2-角门东-2-角门西-2-草桥-2-纪家庙-2-首经贸-2-丰台站-2-泥洼-2-西局-2-六里桥-2-莲花桥-2-公主坟-2-西钓鱼台-2-慈寿寺-2-车道沟-3-长春桥-2-火器营-2-巴沟",
    "11号线": "金安桥-2-北辛安-2-新首钢-2-模式口",
    "12号线": "四季青-2-远大路-2-长春桥-2-苏州桥-2-人民大学-2-大钟寺-2-蓟门桥-2-北太平庄-2-马甸-2-安华桥-2-安贞桥-2-和平西桥-2-光熙门-2-西坝河-2-三元桥",
    "13号线": "西直门-3-大钟寺-3-知春路-2-五道口-3-上地-3-清河站-3-西二旗-3-龙泽-3-回龙观-3-霍营-3-立水桥-3-北苑-3-望京西-3-芍药居-3-光熙门-3-柳芳-3-东直门",
    "14号线": "张郭庄-3-园博园-3-大瓦窑-3-郭公庄-2-大葆台-2-西铁营-2-景风门-2-北京南站-2-陶然桥-2-永定门外-2-景泰-2-蒲黄榆-2-方庄-2-十里河-2-北工大西门-2-平乐园-2-九龙山-2-大望路-2-红庙-2-金台路-2-朝阳公园-2-枣营-2-东风北桥-3-将台-2-望京南-2-阜通-2-望京-3-东湖渠-2-来广营-2-善各庄",
    "15号线": "清华东路西口-2-六道口-2-北沙滩-2-奥林匹克公园-2-安立路-2-大屯路东-3-关庄-2-望京西-2-望京-3-望京东-3-崔各庄-3-马泉营-4-孙河-3-国展-3-花梨坎-3-后沙峪-4-南法信-3-石门-2-顺义-2-俸伯",
    "16号线": "北安河-3-温阳路-2-稻香湖路-2-屯佃-3-永丰-2-永丰南-3-西北旺-2-马连洼-3-农大南路-2-西苑-2-万泉河桥-2-苏州桥-2-万寿寺-2-国家图书馆-2-二里沟-2-甘家口-2-玉渊潭东门-2-木樨地-2-达官营-2-红莲南路-2-丽泽商务区-2-东管头南-2-丰台站-3-看丹-2-榆树庄-2-洪泰庄-2-宛平城",
    "17号线": "未来科学城北-3-未来科学城-3-天通苑东-3-清河营-2-红军营-2-望京西-3-太阳宫-3-西坝河-2-左家庄-2-工人体育场",
    "17号线": "十里河-3-十八里店-4-北神树-3-次渠北-2-次渠-3-嘉会湖",
    "19号线": "牡丹园-2-北太平庄-3-积水潭-4-平安里-4-太平桥-2-牛街-3-景风门-3-草桥-3-新发地-3-新宫",
    "亦庄线": "宋家庄-3-肖村-2-小红门-3-旧宫-2-亦庄桥-2-亦庄文化园-2-万源街-2-荣京东街-2-荣昌东街-2-同济南路-3-经海路-3-次渠南-2-次渠-2-亦庄火车站",
    "房山线": "东管头南-2-首经贸-2-花乡东桥-2-白盆窑-2-郭公庄-3-大葆台-3-稻田-4-长阳-3-篱笆房-2-广阳城-2-良乡大学城北-2-良乡大学城-2-良乡大学城西-3-良乡南关-3-苏庄-2-阎村东",
    "燕房线": "阎村东-2-紫草坞-2-阎村-2-星城-3-大石河东-2-马各庄-3-饶乐府-3-房山城关-3-燕山",
    "S1线": "苹果园-3-金安桥-3-四道桥-3-桥户营-2-上岸-2-栗园庄-3-小园-2-石厂",
    "昌平线": "西土城-2-学院桥-2-六道口-2-清河小营桥-2-学知园-2-六道口-2-上清桥-3-清河站-4-西二旗-5-生命科学园-4-朱辛庄-3-巩华城-4-沙河-3-沙河高教园-3-南邵-3-北邵洼-4-昌平东关-2-昌平-2-十三陵景区-3-昌平西山口",
    "大兴机场线": "草桥-19-大兴新城-20-大兴机场",
    "首都机场线": "北新桥-3-东直门-20-三元桥-20-3号航站楼-5-2号航站楼-15-三元桥",
    "西郊线": "巴沟-3-颐和园西门-3-茶棚-2-万安-3-植物园-3-香山",
}

interchange_station_data_source = [
    "公主坟~1号线-2.25-公主坟~10号线","军事博物馆~9号线-4.00-军事博物馆~1号线","木樨地~1号线-8.00-木樨地~16号线",
    "复兴门~2号线-0.42-复兴门~1号线","复兴门~1号线-2.50-复兴门~2号线","复兴门~1号线-12.00-太平桥~19号线","复兴门~2号线-11.50-太平桥~19号线",
    "西单~1号线-3.50-西单~4号线","王府井~1号线-2.50-王府井~8号线","东单~1号线-3.50-东单~5号线","建国门~2号线-0.50-建国门~1号线",
    "建国门~1号线-0.50-建国门~2号线","建国门~1号线-1.83-建国门~2号线","国贸~1号线-3.33-国贸~10号线","国贸~1号线-4.17-国贸~10号线",
    "大望路~1号线-5.00-大望路~14号线","花庄~1号线-1.33-花庄~7号线","西直门~4号线-4.83-西直门~13号线","西直门~2号线-4.25-西直门~13号线",
    "西直门~4号线-2.00-西直门~2号线","西直门~4号线-0.33-西直门~2号线","西直门~2号线-0.33-西直门~4号线","车公庄~6号线-2.50-车公庄~2号线",
    "车公庄~2号线-1.75-车公庄~6号线","复兴门~2号线-0.42-复兴门~1号线","复兴门~1号线-2.50-复兴门~2号线","复兴门~1号线-12.00-太平桥~19号线",
    "复兴门~2号线-11.50-太平桥~19号线","宣武门~4号线-2.50-宣武门~2号线","宣武门~2号线-1.25-宣武门~4号线","前门~2号线-4.50-前门~8号线",
    "前门~8号线-3.75-前门~2号线","前门~2号线-3.75-前门~8号线","崇文门~5号线-3.00-崇文门~2号线","崇文门~2号线-2.25-崇文门~5号线",
    "建国门~2号线-0.50-建国门~1号线","建国门~1号线-0.50-建国门~2号线","建国门~1号线-1.83-建国门~2号线","朝阳门~6号线-3.00-朝阳门~2号线",
    "朝阳门~2号线-1.17-朝阳门~6号线","东四十条~3号线-2.75-东四十条~2号线","东四十条~2号线-1.50-东四十条~3号线","东直门~13号线-3.50-东直门~2号线",
    "东直门~2号线-6.00-东直门~13号线","雍和宫~2号线-1.33-雍和宫~5号线","雍和宫~5号线-1.67-雍和宫~2号线","雍和宫~5号线-1.83-雍和宫~2号线",
    "鼓楼大街~2号线-3.00-鼓楼大街~8号线","积水潭~2号线-2.83-积水潭~19号线","积水潭~19号线-3.17-积水潭~2号线","东四十条~3号线-2.75-东四十条~2号线",
    "东四十条~2号线-1.50-东四十条~3号线","工人体育场~3号线-2.00-工人体育场~17号线","工人体育场~3号线-0.75-工人体育场~17号线",
    "工人体育场~3号线-1.33-工人体育场~17号线","工人体育场~17号线-1.33-工人体育场~3号线","工人体育场~17号线-0.75-工人体育场~3号线",
    "团结湖~3号线-2.50-团结湖~10号线","团结湖~3号线-2.17-团结湖~10号线","朝阳公园~14号线-1.67-朝阳公园~3号线","朝阳公园~14号线-1.25-朝阳公园~3号线",
    "朝阳公园~3号线-1.25-朝阳公园~14号线","朝阳公园~3号线-1.67-朝阳公园~14号线","朝阳公园~3号线-3.50-朝阳公园~14号线","朝阳公园~3号线-3.17-朝阳公园~14号线",
    "东坝北~12号线-0.17-东坝北~3号线","西苑~4号线-3.00-西苑~16号线","海淀黄庄~4号线-1.17-海淀黄庄~10号线","海淀黄庄~4号线-1.17-海淀黄庄~10号线",
    "人民大学~12号线-2.67-人民大学~4号线","人民大学~12号线-2.50-人民大学~4号线","人民大学~4号线-2.00-人民大学~12号线","人民大学~12号线-2.00-人民大学~4号线",
    "人民大学~12号线-2.50-人民大学~4号线","人民大学~12号线-2.67-人民大学~4号线","国家图书馆~16号线-3.50-国家图书馆~4/9号线",
    "国家图书馆~16号线-3.25-国家图书馆~4/9号线","国家图书馆~4/9号线-0.75-国家图书馆~4/9号线","国家图书馆~4/9号线-0.17-国家图书馆~4/9号线",
    "西直门~4号线-4.83-西直门~13号线","西直门~2号线-4.25-西直门~13号线","西直门~4号线-2.00-西直门~2号线","西直门~4号线-0.33-西直门~2号线",
    "西直门~2号线-0.33-西直门~4号线","平安里~6号线-3.00-平安里~4号线","平安里~6号线-4.67-平安里~19号线","平安里~19号线-7.25-平安里~4号线",
    "西单~1号线-3.50-西单~4号线","宣武门~4号线-2.50-宣武门~2号线","宣武门~2号线-1.25-宣武门~4号线","菜市口~4号线-2.50-菜市口~7号线",
    "菜市口~7号线-0.50-菜市口~4号线","北京南站~4号线-0.67-北京南站~14号线","北京南站~14号线-2.33-北京南站~4号线","角门西~4号线-2.33-角门西~10号线",
    "新宫~19号线-2.33-新宫~4号线","新宫~19号线-2.08-新宫~4号线","立水桥~13号线-2.33-立水桥~5号线","立水桥~13号线-1.67-立水桥~5号线",
    "大屯路东~5号线-4.75-大屯路东~15号线","惠新西街南口~5号线-0.67-惠新西街南口~10号线","惠新西街南口~5号线-0.50-惠新西街南口~10号线",
    "和平西桥~5号线-3.17-和平西桥~12号线","和平西桥~5号线-3.75-和平西桥~12号线","雍和宫~2号线-1.33-雍和宫~5号线","雍和宫~5号线-1.67-雍和宫~2号线",
    "雍和宫~5号线-1.83-雍和宫~2号线","东四~6号线-4.00-东四~5号线","东四~5号线-3.75-东四~6号线","东单~1号线-3.50-东单~5号线","崇文门~5号线-3.00-崇文门~2号线",
    "崇文门~2号线-2.25-崇文门~5号线","磁器口~5号线-2.00-磁器口~7号线","蒲黄榆~5号线-2.17-蒲黄榆~14号线","宋家庄~5号线-1.00-宋家庄~亦庄线",
    "宋家庄~亦庄线-1.75-宋家庄~5号线","宋家庄~10号线-2.00-宋家庄~亦庄线","宋家庄~10号线-2.15-宋家庄~亦庄线","宋家庄~5号线-1.42-宋家庄~10号线",
    "宋家庄~5号线-1.17-宋家庄~10号线","宋家庄~10号线-1.00-宋家庄~5号线","宋家庄~10号线-0.75-宋家庄~5号线","金安桥~6号线-3.00-金安桥~11号线",
    "金安桥~6号线-2.25-金安桥~S1线","金安桥~11号线-4.25-金安桥~S1线","苹果园~6号线-4.00-苹果园~S1线","慈寿寺~6号线-1.33-慈寿寺~10号线",
    "慈寿寺~6号线-0.83-慈寿寺~10号线","慈寿寺~10号线-0.83-慈寿寺~6号线","白石桥南~6号线-0.67-白石桥南~9号线","二里沟~6号线-1.17-二里沟~16号线",
    "车公庄~6号线-2.50-车公庄~2号线","车公庄~2号线-1.75-车公庄~6号线","平安里~6号线-3.00-平安里~4号线","平安里~6号线-4.67-平安里~19号线",
    "平安里~19号线-7.25-平安里~4号线","南锣鼓巷~6号线-1.50-南锣鼓巷~8号线","南锣鼓巷~8号线-1.50-南锣鼓巷~6号线","东四~6号线-4.00-东四~5号线",
    "东四~5号线-3.75-东四~6号线","朝阳门~6号线-3.00-朝阳门~2号线","朝阳门~2号线-1.17-朝阳门~6号线","呼家楼~6号线-0.75-呼家楼~10号线",
    "呼家楼~10号线-0.75-呼家楼~6号线","金台路~6号线-0.75-金台路~14号线","金台路~14号线-2.33-金台路~6号线","北京西站~9/7号线-0.75-北京西站~9/7号线",
    "北京西站~9/7号线-0.17-北京西站~9/7号线","达官营~7号线-3.25-达官营~16号线","广安门内~7号线-10.50-牛街~19号线","菜市口~4号线-2.50-菜市口~7号线",
    "菜市口~7号线-0.50-菜市口~4号线","珠市口~8号线-1.50-珠市口~7号线","珠市口~7号线-3.00-珠市口~8号线","磁器口~5号线-2.00-磁器口~7号线",
    "双井~10号线-2.42-双井~7号线","九龙山~7号线-2.00-九龙山~14号线","九龙山~14号线-0.75-九龙山~7号线","九龙山~7号线-0.75-九龙山~14号线",
    "花庄~1号线-1.33-花庄~7号线","朱辛庄~8号线-1.50-朱辛庄~昌平线","朱辛庄~8号线-0.17-朱辛庄~昌平线","霍营~8号线-3.00-霍营~13号线",
    "霍营~8号线-3.17-霍营~13号线","奥林匹克公园~8号线-4.25-奥林匹克公园~15号线","北土城~8号线-1.42-北土城~10号线","北土城~10号线-0.42-北土城~8号线",
    "安华桥~8号线-4.17-安华桥~12号线","安华桥~8号线-3.92-安华桥~12号线","安华桥~12号线-4.50-安华桥~8号线","鼓楼大街~2号线-3.00-鼓楼大街~8号线",
    "南锣鼓巷~6号线-1.50-南锣鼓巷~8号线","南锣鼓巷~8号线-1.50-南锣鼓巷~6号线","王府井~1号线-2.50-王府井~8号线","前门~2号线-4.50-前门~8号线",
    "前门~8号线-3.75-前门~2号线","前门~2号线-3.75-前门~8号线","珠市口~8号线-1.50-珠市口~7号线","珠市口~7号线-3.00-珠市口~8号线",
    "永定门外~14号线-2.75-永定门外~8号线","国家图书馆~16号线-3.50-国家图书馆~4/9号线","国家图书馆~16号线-3.25-国家图书馆~4/9号线",
    "国家图书馆~4/9号线-0.75-国家图书馆~4/9号线","国家图书馆~4/9号线-0.17-国家图书馆~4/9号线","白石桥南~6号线-0.67-白石桥南~9号线",
    "军事博物馆~9号线-4.00-军事博物馆~1号线","北京西站~9/7号线-0.75-北京西站~9/7号线","北京西站~9/7号线-0.17-北京西站~9/7号线",
    "六里桥~9号线-0.67-六里桥~10号线","七里庄~9号线-0.92-七里庄~14号线","七里庄~9号线-0.50-七里庄~14号线","丰台南路~9号线-1.75-丰台南路~16号线",
    "郭公庄~9号线-0.17-郭公庄~房山线","郭公庄~9号线-1.00-郭公庄~房山线","苏州街~16号线-1.25-苏州街~10号线","海淀黄庄~4号线-1.17-海淀黄庄~10号线",
    "知春路~10号线-2.67-知春路~13号线","知春路~10号线-2.50-知春路~13号线","西土城~10号线-2.75-西土城~昌平线","牡丹园~19号线-3.00-牡丹园~10号线",
    "牡丹园~10号线-2.17-牡丹园~19号线","北土城~8号线-1.42-北土城~10号线","北土城~10号线-0.42-北土城~8号线","惠新西街南口~5号线-0.67-惠新西街南口~10号线",
    "惠新西街南口~5号线-0.50-惠新西街南口~10号线","芍药居~10号线-2.67-芍药居~13号线","芍药居~10号线-3.00-芍药居~13号线","太阳宫~10号线-2.17-太阳宫~17号线",
    "三元桥~12号线-3.58-三元桥~10号线","团结湖~3号线-2.50-团结湖~10号线","团结湖~3号线-2.17-团结湖~10号线","呼家楼~6号线-0.75-呼家楼~10号线",
    "呼家楼~10号线-0.75-呼家楼~6号线","国贸~1号线-3.33-国贸~10号线","国贸~1号线-4.17-国贸~10号线","双井~10号线-2.42-双井~7号线",
    "十里河~10号线-2.83-十里河~17号线","十里河~10号线-2.83-十里河~14号线","十里河~14号线-2.67-十里河~10号线","十里河~10号线-2.50-十里河~14号线",
    "十里河~14号线-4.17-十里河~17号线","十里河~17号线-4.50-十里河~14号线","宋家庄~5号线-1.00-宋家庄~亦庄线","宋家庄~亦庄线-1.75-宋家庄~5号线",
    "宋家庄~10号线-2.00-宋家庄~亦庄线","宋家庄~10号线-2.15-宋家庄~亦庄线","宋家庄~5号线-1.42-宋家庄~10号线","宋家庄~5号线-1.17-宋家庄~10号线",
    "宋家庄~10号线-1.00-宋家庄~5号线","宋家庄~10号线-0.75-宋家庄~5号线","角门西~4号线-2.33-角门西~10号线","草桥~10号线-5.33-草桥~19号线",
    "首经贸~房山线-2.17-首经贸~10号线","首经贸~10号线-1.00-首经贸~房山线","丰台站~10号线-3.00-丰台站~16号线","西局~14号线-0.75-西局~10号线",
    "西局~10号线-1.50-西局~14号线","六里桥~9号线-0.67-六里桥~10号线","公主坟~1号线-2.25-公主坟~10号线","慈寿寺~6号线-1.33-慈寿寺~10号线",
    "慈寿寺~6号线-0.83-慈寿寺~10号线","慈寿寺~10号线-0.83-慈寿寺~6号线","长春桥~12号线-2.75-长春桥~10号线","长春桥~12号线-2.75-长春桥~10号线",
    "苏州桥~12号线-1.50-苏州桥~16号线","苏州桥~12号线-2.00-苏州桥~16号线","人民大学~12号线-2.67-人民大学~4号线","人民大学~12号线-2.50-人民大学~4号线",
    "人民大学~4号线-2.00-人民大学~12号线","人民大学~12号线-2.00-人民大学~4号线","人民大学~12号线-2.50-人民大学~4号线","人民大学~12号线-2.67-人民大学~4号线",
    "大钟寺~13号线-7.83-大钟寺~12号线","蓟门桥~12号线-1.92-蓟门桥~昌平线","蓟门桥~12号线-0.67-蓟门桥~昌平线","蓟门桥~12号线-1.25-蓟门桥~昌平线",
    "蓟门桥~昌平线-1.25-蓟门桥~12号线","蓟门桥~昌平线-0.67-蓟门桥~12号线","北太平庄~12号线-0.75-北太平庄~19号线","北太平庄~19号线-0.75-北太平庄~12号线",
    "北太平庄~19号线-2.00-北太平庄~12号线","安华桥~8号线-4.17-安华桥~12号线","安华桥~8号线-3.92-安华桥~12号线","安华桥~12号线-4.50-安华桥~8号线",
    "和平西桥~5号线-3.17-和平西桥~12号线","和平西桥~5号线-3.75-和平西桥~12号线","光熙门~12号线-5.00-光熙门~13号线","西坝河~12号线-3.50-西坝河~17号线",
    "西坝河~12号线-1.75-西坝河~17号线","西坝河~12号线-2.25-西坝河~17号线","西坝河~17号线-1.75-西坝河~12号线","西坝河~17号线-2.25-西坝河~12号线",
    "三元桥~12号线-3.58-三元桥~10号线","东坝北~12号线-0.17-东坝北~3号线","西直门~4号线-4.83-西直门~13号线","西直门~2号线-4.25-西直门~13号线",
    "西直门~4号线-2.00-西直门~2号线","西直门~4号线-0.33-西直门~2号线","西直门~2号线-0.33-西直门~4号线","大钟寺~13号线-7.83-大钟寺~12号线",
    "知春路~10号线-2.67-知春路~13号线","知春路~10号线-2.50-知春路~13号线","清河站~13号线-1.50-清河站~昌平线","西二旗~13号线-0.75-西二旗~昌平线",
    "西二旗~13号线-0.50-西二旗~昌平线","西二旗~13号线-2.25-西二旗~昌平线","西二旗~13号线-1.00-西二旗~昌平线","霍营~8号线-3.00-霍营~13号线",
    "霍营~8号线-3.17-霍营~13号线","立水桥~13号线-2.33-立水桥~5号线","立水桥~13号线-1.67-立水桥~5号线","望京西~13号线-4.75-望京西~15号线",
    "望京西~13号线-4.92-望京西~15号线","芍药居~10号线-2.67-芍药居~13号线","芍药居~10号线-3.00-芍药居~13号线","光熙门~12号线-5.00-光熙门~13号线",
    "东直门~13号线-3.50-东直门~2号线","东直门~2号线-6.00-东直门~13号线","七里庄~9号线-0.92-七里庄~14号线","七里庄~9号线-0.50-七里庄~14号线",
    "西局~14号线-0.75-西局~10号线","西局~10号线-1.50-西局~14号线","景风门~14号线-3.50-景风门~19号线","北京南站~4号线-0.67-北京南站~14号线",
    "北京南站~14号线-2.33-北京南站~4号线","永定门外~14号线-2.75-永定门外~8号线","蒲黄榆~5号线-2.17-蒲黄榆~14号线","十里河~10号线-2.83-十里河~17号线",
    "十里河~10号线-2.83-十里河~14号线","十里河~14号线-2.67-十里河~10号线","十里河~10号线-2.50-十里河~14号线","十里河~14号线-4.17-十里河~17号线",
    "十里河~17号线-4.50-十里河~14号线","九龙山~7号线-2.00-九龙山~14号线","九龙山~14号线-0.75-九龙山~7号线","九龙山~7号线-0.75-九龙山~14号线",
    "大望路~1号线-5.00-大望路~14号线","金台路~6号线-0.75-金台路~14号线","金台路~14号线-2.33-金台路~6号线","朝阳公园~14号线-1.67-朝阳公园~3号线",
    "朝阳公园~14号线-1.25-朝阳公园~3号线","朝阳公园~3号线-1.25-朝阳公园~14号线","朝阳公园~3号线-1.67-朝阳公园~14号线","朝阳公园~3号线-3.50-朝阳公园~14号线",
    "朝阳公园~3号线-3.17-朝阳公园~14号线","望京~15号线-2.83-望京~14号线","六道口~15号线-2.75-六道口~昌平线","奥林匹克公园~8号线-4.25-奥林匹克公园~15号线",
    "大屯路东~5号线-4.75-大屯路东~15号线","望京西~13号线-4.75-望京西~15号线","望京西~13号线-4.92-望京西~15号线","望京~15号线-2.83-望京~14号线",
    "西苑~4号线-3.00-西苑~16号线","苏州街~16号线-1.25-苏州街~10号线","苏州桥~12号线-1.50-苏州桥~16号线","苏州桥~12号线-2.00-苏州桥~16号线",
    "国家图书馆~16号线-3.50-国家图书馆~4/9号线","国家图书馆~16号线-3.25-国家图书馆~4/9号线","国家图书馆~9号线-0.75-国家图书馆~4号线",
    "国家图书馆~4号线-0.17-国家图书馆~9号线","二里沟~6号线-1.17-二里沟~16号线","木樨地~1号线-8.00-木樨地~16号线","达官营~7号线-3.25-达官营~16号线",
    "东管头南~房山线-2.50-东管头南~16号线","丰台站~10号线-3.00-丰台站~16号线","丰台南路~9号线-1.75-丰台南路~16号线","太阳宫~10号线-2.17-太阳宫~17号线",
    "西坝河~12号线-3.50-西坝河~17号线","西坝河~12号线-1.75-西坝河~17号线","西坝河~12号线-2.25-西坝河~17号线","西坝河~17号线-1.75-西坝河~12号线",
    "西坝河~17号线-2.25-西坝河~12号线","工人体育场~3号线-2.00-工人体育场~17号线","工人体育场~3号线-0.75-工人体育场~17号线",
    "工人体育场~3号线-1.33-工人体育场~17号线","工人体育场~17号线-1.33-工人体育场~3号线","工人体育场~17号线-0.75-工人体育场~3号线",
    "十里河~10号线-2.83-十里河~17号线","十里河~10号线-2.83-十里河~14号线","十里河~14号线-2.67-十里河~10号线",
    "十里河~10号线-2.50-十里河~14号线","十里河~14号线-4.17-十里河~17号线","十里河~17号线-4.50-十里河~14号线",
    "牡丹园~19号线-3.00-牡丹园~10号线","牡丹园~10号线-2.17-牡丹园~19号线","北太平庄~12号线-0.75-北太平庄~19号线",
    "北太平庄~19号线-0.75-北太平庄~12号线","北太平庄~19号线-2.00-北太平庄~12号线","积水潭~2号线-2.83-积水潭~19号线",
    "积水潭~19号线-3.17-积水潭~2号线","平安里~6号线-3.00-平安里~4号线","平安里~6号线-4.67-平安里~19号线",
    "平安里~19号线-7.25-平安里~4号线","牛街~7号线-10.50-牛街~19号线","景风门~14号线-3.50-景风门~19号线",
    "草桥~10号线-5.33-草桥~19号线","新宫~19号线-2.33-新宫~4号线","新宫~19号线-2.08-新宫~4号线",
    "阎村东~房山线-0.17-阎村东~燕房线","郭公庄~9号线-0.17-郭公庄~房山线","郭公庄~9号线-1.00-郭公庄~房山线",
    "首经贸~房山线-2.17-首经贸~10号线","首经贸~10号线-1.00-首经贸~房山线","东管头南~房山线-2.50-东管头南~16号线",
    "朱辛庄~8号线-1.50-朱辛庄~昌平线","朱辛庄~8号线-0.17-朱辛庄~昌平线","西二旗~13号线-0.75-西二旗~昌平线","西二旗~13号线-0.50-西二旗~昌平线",
    "西二旗~13号线-2.25-西二旗~昌平线","西二旗~13号线-1.00-西二旗~昌平线","清河站~13号线-1.50-清河站~昌平线","六道口~15号线-2.75-六道口~昌平线",
    "西土城~10号线-2.75-西土城~昌平线","蓟门桥~12号线-1.92-蓟门桥~昌平线","蓟门桥~12号线-0.67-蓟门桥~昌平线","蓟门桥~12号线-1.25-蓟门桥~昌平线",
    "蓟门桥~昌平线-1.25-蓟门桥~12号线","蓟门桥~昌平线-0.67-蓟门桥~12号线"
]


class BeijingSubwaySystem:
    def __init__(self):
        print("Initializing Beijing Subway Network Data...")
        self.stations = set()
        self.edges = []

        self.hell_stations = {"西直门", "东直门", "国贸", "望京西", "平安里"}

        for line, path in subway_data_source.items():
            parts = path.split("-")
            for i in range(0, len(parts) - 2, 2):
                u, t, v = parts[i], int(parts[i + 1]), parts[i + 2]
                self.stations.add(u)
                self.stations.add(v)
                self.edges.append((u, v, t))

        self.sorted_stations = sorted(list(self.stations))
        self.n = len(self.sorted_stations)
        self.name_to_idx = {name: i for i, name in enumerate(self.sorted_stations)}
        self.idx_to_name = {i: name for i, name in enumerate(self.sorted_stations)}

        matrix_data = [[0] * self.n for _ in range(self.n)]
        for u, v, t in self.edges:
            ui, vi = self.name_to_idx[u], self.name_to_idx[v]
            matrix_data[ui][vi] = t
            matrix_data[vi][ui] = t

        self.graph = Graph(matrix_data)
        print(f"Initialization Complete! Loaded {self.n} stations and {self.graph.count_edges() // 2} track segments.")

    def get_station_id(self, name):
        return self.name_to_idx.get(name)

    def print_path(self, path_indices, detail_type="simple"):
        if not path_indices:
            print("No path found.")
            return

        names = [self.idx_to_name[i] for i in path_indices]
        if detail_type == "simple":
            print(" -> ".join(names))

        detected_hell_stations = [name for name in names if name in self.hell_stations]
        if detected_hell_stations:
            print(
                f"This route involves stations known for difficult, long, or crowded transfers: {', '.join(detected_hell_stations)}"
            )
            print("Please prepare for long walks or stairs.")
            print("This route may not be the best route in real life.")

        return names

    def run_interactive(self):
        while True:
            print("\n" + "=" * 50)
            print("   Beijing Subway Graph Navigation System")
            print("=" * 50)
            print("1. [Dijkstra] Fastest Route (Time Weighted)")
            print("2. [BFS] Least Stops Route")
            print("3. [DFS] Random Exploration Path")
            print("4. [Prim] Calculate MST Cost (Total Network Length)")
            print("5. [Degree] Station Hub Analysis")
            print("6. [Matrix] Algebraic Connectivity Path (CPX Experiment)")
            print("7. [Components] Check Network Connectivity")
            print("8. [Simulation] Simulate Line Disruption (Remove Edge)")
            print("0. Exit")
            print("=" * 50)

            choice = input("Enter option number: ")

            if choice == "0":
                break

            elif choice in ["1", "2", "3", "6"]:
                start_name = input("Enter start station (e.g., 西直门): ")
                end_name = input("Enter end station (e.g., 国贸): ")

                s_id = self.get_station_id(start_name)
                e_id = self.get_station_id(end_name)

                if s_id is None or e_id is None:
                    print(
                        "Error: Station name does not exist. Please check your input."
                    )
                    continue

                if choice == "1":
                    print(
                        f"\nCalculating fastest route from {start_name} to {end_name} (Dijkstra)..."
                    )
                    path, time = self.graph.find_shortest_path_weight(s_id, e_id)
                    if path:
                        print(f"Estimated Time: {time} minutes")
                        print("Route:")
                        self.print_path(path)
                    else:
                        print("Destination unreachable.")

                elif choice == "2":
                    print(
                        f"\nCalculating route with fewest stops from {start_name} to {end_name} (BFS)..."
                    )
                    path = self.graph.find_shortest_path_BFS(s_id, e_id)
                    if path:
                        print(f"Total Stops: {len(path)} stations")
                        self.print_path(path)

                elif choice == "3":
                    print(f"\nSearching for a feasible path (DFS)...")
                    path = self.graph.find_path_DFS(s_id, e_id)
                    self.print_path(path)

                elif choice == "6":
                    print(
                        f"\n[Experimental] Computing path via Matrix Multiplication (CPX)..."
                    )
                    res = self.graph.find_shortest_path_CPX(s_id, e_id)
                    print(f"CPX Result: {res}")

            elif choice == "4":
                print("\nCalculating Minimum Spanning Tree (Prim's Algorithm)...")
                mst, cost = self.graph.minimum_spanning_tree_prim(self.graph.data)
                print(
                    f"Minimum weighted length to connect all {self.n} stations: {cost}"
                )

            elif choice == "5":
                name = input("Enter station name to query: ")
                sid = self.get_station_id(name)
                if sid is not None:
                    out_d, in_d = self.graph.get_degree(sid)
                    neighbors = self.graph.get_neighbors(sid)
                    n_names = [self.idx_to_name[i] for i in neighbors]
                    print(f"\nAnalysis for {name}:")
                    print(f"- Connectivity Degree: {out_d}")
                    print(f"- Neighboring Stations: {', '.join(n_names)}")
                    if out_d > 2:
                        print("- Verdict: This is a Transfer Hub.")
                    else:
                        print("- Verdict: Regular Stop.")

            elif choice == "7":
                print("\nAnalyzing network structure...")
                is_connected = self.graph.connectness()
                components = self.graph.connect_components()
                print(f"Is network fully connected: {is_connected}")
                print(f"Number of Connected Components: {len(components)}")
                if not is_connected:
                    print("Warning: Isolated station groups detected!")

                print("\nChecking Bipartite Property (BFS)...")
                is_bi = self.graph.is_bipartite_BFS()
                print(f"Is Bipartite Graph: {is_bi}")

            elif choice == "8":
                print("\nSimulating Construction/Failure Mode...")
                u_name = input("Enter disruption start station: ")
                v_name = input("Enter disruption end station: ")
                u, v = self.get_station_id(u_name), self.get_station_id(v_name)
                if u is not None and v is not None:
                    print(f"Cutting connection between {u_name} <-> {v_name}...")
                    self.graph.remove_edge(u, v)
                    self.graph.remove_edge(v, u)
                    print("Line segment disrupted. Please replan route to see effects.")

            else:
                print("Invalid input.")


if __name__ == "__main__":
    subway_system = BeijingSubwaySystem()
    try:
        subway_system.run_interactive()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
