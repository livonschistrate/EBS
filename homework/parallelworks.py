import threading, argparse, time, random
from publish import generatePubs
from subscribe import generateSubs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="parallelworks.py does parallel running")
    parser.add_argument('--threads', '-t', default=5, type=int, help="Number of workers/threads to execute the operations")
    parser.add_argument('--settype', '-s', default='p', type=str, help="Type of set to choose: publications (p) or subscriptions (s) or both (b)")
    parser.add_argument('--number', '-n', default=100, type=int, help="Number of pubs/subs to generate")
    args = parser.parse_args()
    
    opertype = {
        'p': generatePubs,
        's': generateSubs
    } 
    threads, totaltime = [], 0
    tp , ts = 0, 0
    
    # case 1 : one thread generates pubs/subs
    if args.threads == 1 and args.settype in ['p', 's']:
        t = threading.Thread(target=opertype[args.settype], args=(args.number,))
        start = time.time()
        t.start()
        t.join()
        end = time.time()
        print("One thread generated {0} {1} in an execution time of {2}".format(args.number,
                                                    "subscriptions" if args.settype == 's' else "publications",
                                                    end-start))
        
    # case 2 : multiple threads generates both pubs/subs
    elif args.threads > 1 and args.settype == 'b':
        start = time.time()
        for i in range(args.threads):
            chosen_operation = random.choice(list(opertype.keys()))
            if chosen_operation == 'p':
                tp += 1 
            else:
                ts += 1
            t = threading.Thread(target=opertype[chosen_operation], args=(args.number,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        print(tp, "threads generated publications")
        print(ts, "threads genereated subscriptions")
        print("We ruled {0} threads of {1} {2}, the execution time is: {3}".format(args.threads, args.number, 
                                                                               "messages",
                                                                               end - start))
    
    # case 3: multiple threads generate only publications/ only subscriptions
    elif args.settype in ['p', 's']:
        start = time.time()
        for i in range(args.threads):
            t = threading.Thread(target=opertype[args.settype], args=(args.number,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        end = time.time()
        print("We ruled {0} threads of {1} {2}, the execution time is: {3}".format(args.threads, args.number, 
                                                                               "subscriptions" if args.settype == 's' else "publications",
                                                                               end - start))