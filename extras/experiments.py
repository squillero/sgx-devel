from multiprocessing import Pool
import time


# The bottleneck of the code which is CPU-bound
def upgrade(n):
    while n >= 0:
        n -= 1

if __name__ == '__main__':
    number = 1_000_000_000

    start = time.time()
    upgrade(number)
    end = time.time()
    print('Time taken in seconds ', end - start)

    start = time.time()
    pool = Pool(processes=4)
    r1 = pool.apply_async(upgrade, [number//4])
    r2 = pool.apply_async(upgrade, [number//4])
    r3 = pool.apply_async(upgrade, [number//4])
    r4 = pool.apply_async(upgrade, [number//4])
    pool.close()
    pool.join()
    end = time.time()
    print('Time taken in seconds ', end - start)


   #> Time taken in seconds - 0.10114145278930664
