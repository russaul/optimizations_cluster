import random
from copy import copy, deepcopy
import time
import configparser

alpha = 1
mu = 1
standart = 0.2
n = 0


class Server():
    def __init__(self, core: int, memory: int, id = 0):
        self.core = core
        self.memory = memory
        self.vir_mac = []
        self.active = True
        self.id = id
        self.free_mem = 0
        self.free_core = 0

    def check_size(self, vm_new):
        memory = 0
        core = 0
        for i in self.vir_mac:
            memory = memory + i.memory
            core = core + i.core
        memory = memory + vm_new.memory
        core = core + vm_new.core
        if self.memory < memory:
            return False
        elif self.core < core:
            return False
        else:
            return True

    def deactivation(self):
        if len(self.vir_mac) == 0:
            self.active = False
            return False
        return True

    def server_inf(self):
        f = open('server_inf.txt', 'a')
        f.write("\n Server #" + str(self.id) + "\n")
        f.write("Core (server): " + str(self.core) + "\n")
        f.write("Memory (server): " + str(self.memory) + "\n")
        f.write("Free_core: " + str(self.free_core) + "\n")
        f.write("Free_memory: " + str(self.free_mem) + "\n")
        f.write("     Virtual machines: " + "\n")
        for i in self.vir_mac:
            f.write("Virtual machine #" + str(i.id) + "\n")
            f.write("-------Core: " + str(i.core) + "\n")
            f.write("-------Memory: " + str(i.memory) + "\n")
        f.close()
        print()
        print("Server #", self.id)
        print("Core (server): ", self.core)
        print("Memory (server): ", self.memory)
        print("Free_core: ", self.free_core)
        print("Free_memory: ", self.free_mem)
        print("     Virtual machines: ")
        for i in self.vir_mac:
            print("Virtual machine #", i.id)
            print("-------Core: ", i.core)
            print("-------Memory: ", i.memory)
        print()


class VirtMac():
    def __init__(self, core: int, memory: int, id = 0):
        self.core = core
        self.memory = memory
        self.id = id


def read_cfg():
    config = configparser.ConfigParser()
    config.read("start.ini")
    regime = config["General"]["regime"]
    vm_cfg = config["VirtMac"]
    vms = []
    for i in range(1, int(vm_cfg["count_type"]) + 1):
        vms.append(VirtMac(int(vm_cfg[str(i) + "_core"]), int(vm_cfg[str(i) + "_memory"])))
    return regime, vms


def read_pack():
    global n
    config = configparser.ConfigParser()
    config.read("start.ini")
    n = int(config["Pack"]["budget_migration"])


def read_online():
    config = configparser.ConfigParser()
    config.read("start.ini")
    gen_time = float(config["Online"]["gen_time"])
    limit_calls = int(config["Online"]["limit_calls"])
    regime = config["Online"]["regime"]
    return gen_time, limit_calls, regime


def create_cluster():
    config = configparser.ConfigParser()
    config.read("start.ini")
    srv_cfg = config["Servers"]
    cluster = []
    counter = 1
    for i in range(1, int(srv_cfg["count_type"])+1):
        for j in range(1, int(srv_cfg[str(i)+"_count"])+1):
            cluster.append(Server(int(srv_cfg[str(i)+"_core"]), int(srv_cfg[str(i)+"_memory"]), counter))
            counter += 1
    random.shuffle(cluster)
    return cluster


def create_vms():
    config = configparser.ConfigParser()
    config.read("start.ini")
    vm_cfg = config["VirtMac"]
    vms = []
    counter = 1
    for i in range(1, int(vm_cfg["count_type"])+1):
        for j in range(1, int(vm_cfg[str(i)+"_count"])+1):
            vms.append(VirtMac(int(vm_cfg[str(i)+"_core"]), int(vm_cfg[str(i)+"_memory"]), counter))
            counter += 1
    random.shuffle(vms)
    return vms


def heapify_core(vms: list, heap_size, root_index):
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2
    if left_child < heap_size and vms[left_child].core > vms[largest].core:
        largest = left_child
    if right_child < heap_size and vms[right_child].core > vms[largest].core:
        largest = right_child
    if largest != root_index:
        vms[root_index], vms[largest] = vms[largest], vms[root_index]
        heapify_core(vms, heap_size, largest)


def heapify_memory(vms: list, heap_size, root_index):
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2
    if left_child < heap_size and vms[left_child].core > vms[largest].core:
        largest = left_child
    if right_child < heap_size and vms[right_child].core > vms[largest].core:
        largest = right_child
    if largest != root_index:
        vms[root_index], vms[largest] = vms[largest], vms[root_index]
        heapify_memory(vms, heap_size, largest)


def heapify_free_core(vms: list, heap_size, root_index):
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2
    if left_child < heap_size and vms[left_child].free_core > vms[largest].free_core:
        largest = left_child
    if right_child < heap_size and vms[right_child].free_core > vms[largest].free_core:
        largest = right_child
    if largest != root_index:
        vms[root_index], vms[largest] = vms[largest], vms[root_index]
        heapify_free_core(vms, heap_size, largest)


def heap_sort(vms: list, flag: str):
    n = len(vms)
    if flag == "core":
        for i in range(n, -1, -1):
            heapify_core(vms, n, i)
        for i in range(n - 1, 0, -1):
            vms[i], vms[0] = vms[0], vms[i]
            heapify_core(vms, i, 0)
    if flag == "memory":
        for i in range(n, -1, -1):
            heapify_memory(vms, n, i)
        for i in range(n - 1, 0, -1):
            vms[i], vms[0] = vms[0], vms[i]
            heapify_memory(vms, i, 0)
    if flag == "free_core":
        for i in range(n, -1, -1):
            heapify_free_core(vms, n, i)
        for i in range(n - 1, 0, -1):
            vms[i], vms[0] = vms[0], vms[i]
            heapify_free_core(vms, i, 0)


def clustering(vms: list, cluster: list, map_cluster: dict):
    n = 0
    num_srv = 0
    for i in range(0, len(vms)):
        if num_srv == len(cluster):
            num_srv = 0
        while num_srv < len(cluster):
            if n > len(cluster):
                print("Invicible to pack!")
                return [], map_cluster
            if cluster[num_srv].check_size(vms[i]):
                cluster[num_srv].vir_mac.append(vms[i])
                map_cluster[vms[i].id] = cluster[num_srv]
                n = 0
                num_srv += 1
                break
            else:
                n += 1
                num_srv += 1
                if num_srv == len(cluster):
                    num_srv = 0
    else:
        return cluster, map_cluster


def cluster_copy(cluster: list):
    new_cluster = []
    for i in cluster:
        srv = Server(i.core, i.memory)
        for j in i.vir_mac:
            vm = VirtMac(j.core, j.memory, j.id)
            srv.vir_mac.append(vm)
        new_cluster.append(srv)
    return new_cluster


def first_fit_decreasing(cluster: list, map_cluster: dict):
    num_migration = 0
    new_cluster = cluster
    list_vms = []
    for i in new_cluster:
        list_vms += i.vir_mac
    heap_sort(list_vms, "core")
    list_vms.reverse()
    heap_sort(new_cluster, "core")
    new_cluster.reverse()
    for i in range(0, len(list_vms)):
        for j in range(0, len(new_cluster)):
            if new_cluster[j].vir_mac.count(list_vms[i]) > 0:
                map_cluster[list_vms[i].id] = new_cluster[j]
                break
            else:
                if new_cluster[j].check_size(list_vms[i]):
                    new_cluster[j].vir_mac.append(list_vms[i])
                    map_cluster.get(list_vms[i].id).vir_mac.remove(list_vms[i])
                    map_cluster[list_vms[i].id] = new_cluster[j]
                    num_migration += 1
                    break
                else:
                    continue
    return map_cluster, num_migration


def calculating_weight(map_n: dict):
    for i in range(1, len(map_n)):
        a = map_n.get(i)


def find_cur_server(cur_id: int, servers: list):
    for i in servers:
        if i.id == cur_id:
            return i
    return None


def check_free_servers(servers: dict, vm: VirtMac):
    free_srv = []
    for i in servers:
        if servers.get(i)[0] >= vm.core and servers.get(i)[1] >= vm.memory and servers.get(i)[2]:
            free_srv.append(i)
    return free_srv


def computing_free_space(srv: Server):
    core = 0
    memory = 0
    for i in srv.vir_mac:
        core += i.core
        memory += i.memory
    srv.free_core = srv.core - core
    srv.free_mem = srv.memory - memory
    if srv.free_core == srv.core:
        srv.active = False


def computing_free_cluster(cluster: list):
    for i in cluster:
        computing_free_space(i)


def _sort_free_servers(free_dict: dict, servers_dict: dict, servers: dict):
    for i in free_dict:
        tmp = copy(free_dict.get(i))
        new_tmp = []
        for j in tmp:
            new_tmp.append([j]+servers_dict.get(j))
        new_tmp.sort(key=lambda lst: lst[1])
        tmp = []
        for j in new_tmp:
            tmp.append(j[0])
        tmp = sorted(tmp, key=lambda i: servers.get(i).core, reverse=True)
        free_dict[i] = copy(tmp)
    return free_dict


def loop_1(servers: dict, servers_dict: dict, vms_dict: dict, map_cluster: dict, free_dict: dict, weight_0: list, num_migr: int, level):
    global alpha, mu, standart, n
    free_core, free_mem, memory, core = 0, 0, 0, 0
    for i in servers:
        if servers_dict.get(i)[2]:
            free_core += servers_dict.get(i)[0]
            free_mem += servers_dict.get(i)[1]
            memory += servers.get(i).memory
            core += servers.get(i).core
    level += 1
    active = 0
    for i in servers_dict:
        if servers_dict.get(i)[2]:
            active += 1
    if num_migr >= n:
        if active < weight_0[0]:
            weight_0 = [active, num_migr]
        return weight_0
    if active < weight_0[0] or num_migr > weight_0[1]:
        if active+num_migr < weight_0[0] + weight_0[1]:
            weight_0 = [active, num_migr]
            print(weight_0)
            return weight_0
    if len(vms_dict) == 0:
        if active < weight_0[0]:
            weight_0 = [active, num_migr]
            print(weight_0)
        return weight_0
    keys = list(vms_dict.keys())
    cur_id = keys[0]
    for i in free_dict:
        if len(free_dict.get(i)) < len(free_dict.get(cur_id)):
            cur_id = i
    tmp_srvs = free_dict.get(cur_id)
    for i in tmp_srvs:
        tmp_map = deepcopy(map_cluster)
        tmp_vms = deepcopy(vms_dict)
        tmp_serv_dict = deepcopy(servers_dict)
        tmp_free_dict = deepcopy(free_dict)
        tmp_num_migr = num_migr
        if servers.get(i).id == servers.get(tmp_map.get(cur_id)).id:
            tmp_vms.pop(cur_id)
            tmp_free_dict.pop(cur_id)
        else:
            tmp_num_migr += 1
            tmp_serv_dict.get(i)[0] -= tmp_vms.get(cur_id).core
            tmp_serv_dict.get(i)[1] -= tmp_vms.get(cur_id).memory
            tmp_serv_dict.get(tmp_map.get(cur_id))[0] += tmp_vms.get(cur_id).core
            tmp_serv_dict.get(tmp_map.get(cur_id))[1] += tmp_vms.get(cur_id).memory
            tmp_map[cur_id] = i
            for j in tmp_serv_dict:
                if tmp_serv_dict.get(j)[0] == servers.get(j).core:
                    tmp_serv_dict.get(j)[2] = False
            tmp_vms.pop(cur_id)
            a = []
            for j in tmp_vms:
                a.append(tmp_vms.get(j))
            for j in a:
                tmp_free_dict[j.id] = check_free_servers(tmp_serv_dict, j)
            tmp_free_dict = _sort_free_servers(tmp_free_dict, tmp_serv_dict, servers)
            tmp_free_dict.pop(cur_id)
        weight_0 = loop_1(servers, tmp_serv_dict, tmp_vms, tmp_map, tmp_free_dict, weight_0, tmp_num_migr, level)
    return weight_0


def new_alg(cluster: list, map_cluster: dict, weight_0: list):
    vms = []
    for i in cluster:
        vms += i.vir_mac
    vms.sort(key=lambda vm: vm.core, reverse=True)
    new_map = {}
    vms_dict = {}
    free_dict = {}
    servers = {}
    servers_dict = {}
    for i in cluster:
        servers[i.id] = i
    for i in servers:
        servers_dict[servers.get(i).id] = [servers.get(i).free_core, servers.get(i).free_mem, servers.get(i).active]
    for i in map_cluster:
        for j in servers:
            if servers.get(j) == map_cluster.get(i):
                new_map[i] = j
    for i in vms:
        free_dict[i.id] = check_free_servers(servers_dict, i)
    free_dict = _sort_free_servers(free_dict, servers_dict, servers)
    for i in vms:
        vms_dict[i.id] = i
    num_migr = 0
    level = 0
    return loop_1(servers, servers_dict, vms_dict, new_map, free_dict, weight_0, num_migr, level)


def generating(vms: list, vm_list: list):
    tmp = vms[random.randint(0, len(vms) - 1)]
    new_id = 0
    for i in vm_list:
        if i.id > new_id:
            new_id = i.id
    new_id += 1
    vm = VirtMac(tmp.core, tmp.memory, id=new_id)
    vm_list.append(vm)
    return vm, vm_list


def first_fit(cluster: list, cur_vm: VirtMac, map_cluster: dict):
    correct = False
    for i in cluster:
        if i.check_size(cur_vm):
            i.vir_mac.append(cur_vm)
            i.free_core -= cur_vm.core
            i.free_mem -= cur_vm.memory
            map_cluster[cur_vm.id] = i
            correct = True
            break
    if not correct:
        print("No server can host this machine")
        return False
    return True


def optimal_fit(cluster: list, cur_vm: VirtMac, map_cluster: dict):
    correct = False
    cluster.sort(key=lambda i: i.free_core)
    for i in cluster:
        if i.check_size(cur_vm):
            i.vir_mac.append(cur_vm)
            i.free_core -= cur_vm.core
            i.free_mem -= cur_vm.memory
            map_cluster[cur_vm.id] = i
            correct = True
            break
    if not correct:
        print("No server can host this machine")
        return False
    return True


def online_alg(cluster: list, map_cluster: dict, vms: list, vm_list: list):
    gen_time, limit_calls, regime = read_online()
    vm, vm_list = generating(vms, vm_list)
    first_fit(cluster, vm, map_cluster)
    start = time.time()
    count = 0
    ok = True
    while True:
        if count >= limit_calls:
            print("Maximum number of generations reached")
            break
        if not ok:
            break
        if (time.time() - start) >= gen_time:
            vm, vm_list = generating(vms, vm_list)
            start = time.time()
            if regime == "first":
                count += 1
                ok = first_fit(cluster, vm, map_cluster)
            elif regime == "optimal":
                count += 1
                ok = optimal_fit(cluster, vm, map_cluster)


if __name__ == '__main__':
    regime, vm = read_cfg()
    cluster = create_cluster()
    vms = create_vms()

    map_cluster = {}
    cluster, map_cluster = clustering(vms, cluster, map_cluster)
    if len(cluster) == 0:
        exit(0)
    computing_free_cluster(cluster)
    weight = [len(cluster), 0]

    if regime == "pack":
        start_time = time.time()
        read_pack()
        weight = new_alg(cluster, map_cluster, weight)
        print(weight)
        if weight[1] == len(vms):
            print("Don't find normal clustering")
        print("--- %s seconds ---" % (time.time() - start_time))
    elif regime == "online":
        online_alg(cluster, map_cluster, vm, vms)
        computing_free_cluster(cluster)
        for i in cluster:
            i.server_inf()


