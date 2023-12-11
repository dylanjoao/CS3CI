import pandas as pd
import numpy as np
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from threading import Thread
from baseline import evolution_search
from novel import novel_search
from csp_order import CSP, CSP_Novel
from pprint import pprint


if __name__ == '__main__':

    csp_baseline = CSP(36, 
            [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67],
            [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17],
            5,
            [120, 115, 110, 105, 100],
            [12, 11.5, 11, 10.5, 10]
            )

    csp_novel = CSP_Novel(36, 
            [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67],
            [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17],
            5,
            [120, 115, 110, 105, 100],
            [12, 11.5, 11, 10.5, 10]
            )

    threads = []
    full_data = []
    episodes = 3
    duration = 1.0

    algo = novel_search
    # args=(full_data, csp_novel, 20, csp_novel.random_solution, csp_novel.evaluate, duration, 0)
    args=(full_data, csp_novel, 3, 2, csp_novel.random_solution, csp_novel.evaluate, duration, 0)

    # # Start threads 
    # for i in range(episodes): 
    #     t = Thread(target=algo, args=args)
    #     t.start()
    #     threads.append(t)

    # # Wait all threads to finish
    # for t in threads:
    #     t.join()

    result =[]
    with ProcessPoolExecutor(max_workers=5) as exe:    
        exe.submit(algo, args)
        result = exe.map(algo,values)

    data = {
        "ep_best_fitness": [],
        "gen_found_at": [],
        "time_found_at": [],
        "avg_waste": [],
        "avg_cost": []
        } 


    index = 0
    for episode_data, generation_data in full_data:
        data["ep_best_fitness"].append(episode_data["best_fitness"])
        data["gen_found_at"].append(episode_data["gen_found_at"])
        data["time_found_at"].append(episode_data["time_found_at"])
        data["avg_waste"].append( np.mean(episode_data["waste"]) )
        data["avg_cost"].append( np.mean(episode_data["cost"]) )

        gen_data = { "gen_best_fitness": [], "time_found_at": [] }
        for gen in generation_data:
            gen_data["gen_best_fitness"].append(gen[0])
            gen_data["time_found_at"].append(gen[1])

        df = pd.DataFrame(gen_data)
        df.to_csv(f'./data/novel_generations/novel_gens_for_ep_{index}.csv', index=True)
        index += 1


    df = pd.DataFrame(data)

    # # Save the dataframe to a CSV file
    df.to_csv('./data/novel_episodes.csv', index=True)
