import random
import matplotlib.pyplot  as plt
from copy import copy

alpha = 1
mu = 1
standart = 0.2

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
            heapify_core(vms, n, i)
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

def check_free_servers(cluster: list, vm: VirtMac):
    free_srv = []
    for i in cluster:
        if i.free_core > vm.core and i.free_mem > vm.memory:
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

def loop(servers: dict, vms: list, map_cluster: dict, free_dict: dict, weight_0: list, active: int, num_migr: int):
    tmp_active = active
    print(num_migr)
    for j in servers:
        if not servers.get(j)[2]:
            tmp_active -= 1
    global standart
    global alpha, mu
    if alpha * tmp_active + mu * num_migr <= mu * weight_0[1] + alpha * weight_0[0]:
        free_core, free_mem, memory, core = 0, 0, 0, 0
        for i in servers:
            if servers.get(i)[2]:
                free_core += servers.get(i)[0]
                free_mem += servers.get(i)[1]
                memory += i.memory
                core += i.core
        if (free_core + free_mem) / (core + memory) <= standart:
            weight_0 = [tmp_active, num_migr]
            return map_cluster, num_migr, weight_0
    tmp_map_cluster = map_cluster
    tmp_num_migr = num_migr
    if len(vms) == 0:
        if alpha*tmp_active + mu*num_migr <= mu*weight_0[1] + alpha*weight_0[0]:
            free_core, free_mem, memory, core = 0, 0, 0, 0
            for i in servers:
                if servers.get(i)[2]:
                    free_core += servers.get(i)[0]
                    free_mem += servers.get(i)[1]
                    memory += i.memory
                    core += i.core
            if (free_core + free_mem)/(core + memory) <= standart:
                weight_0 = [tmp_active, num_migr]
        return map_cluster, num_migr, weight_0
    vm = vms[0]
    tmp_srv = copy(free_dict.get(vm.id))
    for i in tmp_srv:
        if servers.get(i)[2] == False:
            continue
        tmp_free_dict = copy(free_dict)
        tmp_vms = copy(vms)
        tmp_map_cluster = copy(map_cluster)
        tmp_servers = copy(servers)
        tmp_num_migr = num_migr
        if i.vir_mac.count(vm) == 1:
            tmp_vms.remove(vm)
        else:
            tmp_num_migr += 1
            tmp_servers.get(i)[0] -= vm.core
            tmp_servers.get(i)[1] -= vm.memory
            tmp_servers.get(tmp_map_cluster.get(vm.id))[0] += vm.core
            tmp_servers.get(tmp_map_cluster.get(vm.id))[1] += vm.memory
            tmp_map_cluster[vm.id] = i
            tmp_vms.remove(vm)
            new_servers = []
            for j in tmp_servers:
                if tmp_servers.get(j)[0] == j.core:
                    tmp_servers.get(j)[2] = False
                    continue
                new_servers.append(j)
            for j in tmp_vms:
                tmp_free_dict[j.id] = check_free_servers(new_servers, j)
                heap_sort(tmp_free_dict.get(j.id), "free_core")
        tmp_map_cluster, tmp_num_migr, weight_0 = loop(tmp_servers, tmp_vms, tmp_map_cluster, tmp_free_dict, weight_0, active, tmp_num_migr)
    return tmp_map_cluster, tmp_num_migr, weight_0

def new_alg(cluster: list, map_cluster: dict, weight_0: list):
    vms = []
    for i in cluster:
        vms += i.vir_mac
    heap_sort(vms, "core")
    vms.reverse()
    free_dict = {}
    for i in vms:
        free_dict[i.id] = check_free_servers(cluster, i)
        heap_sort(free_dict.get(i.id), "free_core")
    servers = {}
    for i in cluster:
        servers[i] = [i.free_core, i.free_mem, i.active]
    num_migr = 0
    active = len(cluster)
    return loop(servers, vms, map_cluster, free_dict, weight_0, active, num_migr)


if __name__ == '__main__':
    servers = [Server(100, 500), Server(150, 1000)]
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
    new_map, num_migr, weight = new_alg(cluster, map_cluster, weight)
    print(weight)
