from itertools import islice
#check that talk https://www.youtube.com/watch?v=M-UcUs7IMIM&feature=youtu.be


def even_nums():
    num = 20
    while True:
        yield  num
        num += 2


def print_val(coro):
    for i in coro:
        print("val is :", i)
        yield i

    raise StopIteration('done')

def odd_nums():
    num = 1
    while True:
        yield num
        num += 2


def get_chars():
    for x in "hellothisisaverylongstring":
        yield x

def get_chars_error():
    for x in "weee":
        yield x
    raise Exception("Error happened in get_chars_error function")

class Task:

    def __init__(self, name, coroutine):
        self.routine = coroutine
        self.name = name

    def __str__(self):
        return self.name

class Sched:
    def __init__(self):
        self.tasks = []
        self.tasks_success = {}
        self.tasks_failure = {}

    def run_till_complete(self):

        while len(self.tasks) > 0:
            for idx, t in enumerate(self.tasks):
                tsk = self.tasks[idx]
                print("running Task {}:: ".format(str(tsk)))
                try:
                    yielded = next(tsk.routine)
                except StopIteration as e: # completed with value.
                    # completed
                    print("task completeed ", tsk.name)
                    self.tasks_success[tsk.name] = e.value
                    self.tasks.remove(tsk)
                except Exception as e:     # failed with exception
                    print("failed with exception ", str(e))
                    self.tasks_failure[tsk.name] = e
                    self.tasks.remove(tsk)
                else:
                    print("Task is yielding..")


    def add_task(self, tsk):
        self.tasks.append(tsk)


def main():
    sched = Sched()
    tsk1 = Task('print_even', print_val(islice(even_nums(), 5)))
    sched.add_task(tsk1)
    tsk2 = Task('print_odd', print_val(islice(odd_nums(), 5)))
    sched.add_task(tsk2)

    tsk3 = Task('print_chars', print_val(islice(get_chars(), 5)))
    sched.add_task(tsk3)


    tsk4 = Task('print_chars_fail', print_val(islice(get_chars_error(), 5)))
    sched.add_task(tsk4)


    sched.run_till_complete()

    print(sched.tasks_success)
    print(sched.tasks_failure)

main()
