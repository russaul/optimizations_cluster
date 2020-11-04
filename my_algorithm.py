import random
import matplotlib.pyplot  as plt
from copy import copy, deepcopy
import time

alpha = 1
mu = 5
standart = 0.2
n = 2

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

    def server_inf(self, numb=0):
        print("Server #", self.id)
        print("Core (server): ", self.core)
        print("Memory (server): ", self.memory)
        print("     Virtual machines: ")
        n = 1
        for i in self.vir_mac:
            print("Virtual machine #", i.id)
            print("-------Core: ", i.core)
            print("-------Memory: ", i.memory)
            n += 1
        print()

class VirtMac():
    def __init__(self, core: int, memory: int, id = 0):
        self.core = core
        self.memory = memory
        self.id = id

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


def loop_1(servers: dict, servers_dict: dict, vms_dict: dict, map_cluster: dict, free_dict: dict, weight_0: list, num_migr: int):
    global alpha, mu, standart, n
    active = 0
    for i in servers_dict:
        if servers_dict.get(i)[2] == True:
            active += 1
    if num_migr == n:
        if active < weight_0[0]:
            weight_0 = [active, num_migr]
            print(weight_0)
        return weight_0
    free_core, free_mem, memory, core = 0, 0, 0, 0
    for i in servers:
        if servers_dict.get(i)[2]:
            free_core += servers_dict.get(i)[0]
            free_mem += servers_dict.get(i)[1]
            memory += servers.get(i).memory
            core += servers.get(i).core
    if len(vms_dict) == 0:
        if num_migr == n:
            if active < weight_0[0]:
                weight_0 = [active, num_migr]
                print(weight_0)
        return weight_0
    keys = list(vms_dict.keys())
    cur_id = keys[0]
    tmp_srvs = free_dict.get(cur_id)
    for i in tmp_srvs:
        tmp_map = deepcopy(map_cluster)
        tmp_vms = deepcopy(vms_dict)
        tmp_serv_dict = deepcopy(servers_dict)
        tmp_free_dict = deepcopy(free_dict)
        tmp_num_migr = num_migr
        if servers.get(i).id == servers.get(tmp_map.get(cur_id)).id:
            tmp_vms.pop(cur_id)
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
        weight_0 = loop_1(servers, tmp_serv_dict, tmp_vms, tmp_map, tmp_free_dict, weight_0, tmp_num_migr)
    return weight_0


def new_alg(cluster: list, map_cluster: dict, weight_0: list):
    vms = []
    for i in cluster:
        vms += i.vir_mac
    heap_sort(vms, "core")
    new_map = {}
    vms.reverse()
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
    for i in vms:
        vms_dict[i.id] = i
    num_migr = 0
    # for i in vms_dict:
    #     print(i)
    weight_0 = [len(servers), len(vms_dict)]
    return loop_1(servers, servers_dict, vms_dict, new_map, free_dict, weight_0, num_migr)


if __name__ == '__main__':
    start_time = time.time()
    servers = [Server(100, 500), Server(15, 1000)]
    vm = [VirtMac(4, 16), VirtMac(8, 32), VirtMac(16, 32)]
    t = int(input("Insert count of servers in cluster: \n"))
    c_vm = int(input("Insert count of virtual machine: \n"))

    cluster = []
    vms = []
    for i in range(t):
        tmp = servers[random.randint(0, len(servers) - 1)]
        cluster.append(Server(tmp.core, tmp.memory, id=i+1))
    for i in range(c_vm):
        tmp = vm[random.randint(0, len(vm)-1)]
        vms.append(VirtMac(tmp.core, tmp.memory, id=i+1))

    map_cluster = {}
    cluster, map_cluster = clustering(vms, cluster, map_cluster)
    if len(cluster) == 0:
        exit(0)
    new_map = {}
    new_cluster = cluster_copy(cluster)
    for i in new_cluster:
        for j in i.vir_mac:
            new_map[j.id] = i
    new_map, num_migr = first_fit_decreasing(new_cluster, new_map)
    act_serv = 0
    for i in new_cluster:
        i.deactivation()
        if i.active == True:
            act_serv += 1
    weight = [act_serv, num_migr]
    print(weight)
    computing_free_cluster(cluster)
    weight = new_alg(cluster, map_cluster, weight)
    print(weight)
    print("--- %s seconds ---" % (time.time() - start_time))
