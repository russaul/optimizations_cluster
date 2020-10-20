import random
import matplotlib.pyplot  as plt

class Server():
    def __init__(self, core: int, memory: int, id = 0):
        self.core = core
        self.memory = memory
        self.vir_mac = []
        self.active = True
        self.id = id

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

def heapify(vms: list, heap_size, root_index):
    largest = root_index
    left_child = (2 * root_index) + 1
    right_child = (2 * root_index) + 2
    if left_child < heap_size and vms[left_child].core > vms[largest].core:
        largest = left_child
    if right_child < heap_size and vms[right_child].core > vms[largest].core:
        largest = right_child
    if largest != root_index:
        vms[root_index], vms[largest] = vms[largest], vms[root_index]
        heapify(vms, heap_size, largest)

def heap_sort(vms: list):
    n = len(vms)
    for i in range(n, -1, -1):
        heapify(vms, n, i)
    for i in range(n - 1, 0, -1):
        vms[i], vms[0] = vms[0], vms[i]
        heapify(vms, i, 0)

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

def first_fit_decreasing(cluster: list, map_cluster: dict):
    num_migration = 0
    new_cluster = cluster
    list_vms = []
    for i in new_cluster:
        list_vms += i.vir_mac
    heap_sort(list_vms)
    list_vms.reverse()
    heap_sort(new_cluster)
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
    return new_cluster, num_migration


if __name__ == '__main__':
    servers = [Server(100, 500), Server(15, 1000)]
    vm = [VirtMac(4, 16), VirtMac(8, 32), VirtMac(16, 32)]
    t = int(input("Insert count of servers in cluster: \n"))
    c_vm = int(input("Insert count of virtual machine: \n"))
    # t_start = 200
    # c_vm_start = 1000
    # migrations = []
    # count_servers = []
    # active_servers = []
    # for a in range(1, 150):
    #     t = t_start
    #     c_vm = c_vm_start
    #     cluster = []
    #     vms = []
    #     for i in range(t):
    #         tmp = servers[random.randint(0, len(servers) - 1)]
    #         cluster.append(Server(tmp.core, tmp.memory, id=i + 1))
    #     for i in range(c_vm):
    #         tmp = vm[random.randint(0, len(vm) - 1)]
    #         vms.append(VirtMac(tmp.core, tmp.memory, id=i + 1))
    #     map_cluster = {}
    #     cluster, map_cluster = clustering(vms, cluster, map_cluster)
    #     if len(cluster) == 0:
    #         continue
    #     # print("FFD--------------------------------------------------------------- ")
    #     new_cluster, count_mig = first_fit_decreasing(cluster, map_cluster)
    #     for i in new_cluster:
    #         i.deactivation()
    #     act = 0
    #     for i in new_cluster:
    #         if i.active:
    #             act += 1
    #     active_servers.append(act)
    #     # print("Active servers: ", act)
    #     # print("Count of migration: ", count_mig)
    #     count_servers.append(len(cluster))
    #     migrations.append(count_mig)
    # plt.title("FFD")
    # # plt.xlabel("Servers")
    # plt.ylabel("Active Servers")
    # plt.plot(active_servers)
    # # plt.show()
    # plt.savefig("Active_server_test")
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
    for i in cluster:
        i.server_inf()
    print("FFD--------------------------------------------------------------- ")
    new_cluster, count_mig = first_fit_decreasing(cluster, map_cluster)
    for i in new_cluster:
        i.deactivation()
    for i in new_cluster:
         i.server_inf()
    act = 0
    for i in new_cluster:
        if i.active:
            act += 1
    print("Active servers: ", act)
    print("Count of migration: ", count_mig)