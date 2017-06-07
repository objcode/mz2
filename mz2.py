from mz2 import grid, btree, sidewinder, random_walk, random_adjacent, backtrack, gui_runner, png_drawer, wilson, hunt_and_kill, growing_tree, distances

import time
import argparse

import sys
from colorama import init, Style, Fore

reload(sys)
sys.setdefaultencoding("utf-8")

def print_runner(fn):
    def named(grid, **kwargs):
        init()
        gen = fn(grid, **kwargs)
        for trial in gen:
            print(Style.RESET_ALL)
            time.sleep(0.05)
            trial.hilite(Fore.RED + '*' + Style.RESET_ALL)
            print(chr(27) + "[2J")
            print(grid)
            trial.hilite(None)
        print(chr(27) + "[2J")
        print(grid)
    return named

def silent_runner(last_print = False):
    def closure(fn):
        def named(grid, **kwargs):
            count = 0
            for trial in fn(grid, **kwargs):
                count += 1
                if count % 1000 == 0:
                    print('.'),
                    sys.stdout.flush()
                pass
            if last_print:
                print grid
        return named
    return closure

def write_file(path, grid):
    png_drawer.PngDrawer(path, grid).draw();

def draw_longest_path(grid, silent=True):
    grid.draw_longest_path()
    if not silent:
        print grid

def gen_growing_tree(args):
    options = {
        'random': growing_tree.RANDOM,
        'first': growing_tree.FIRST,
        'last': growing_tree.LAST,
    }

    selector = options.get(args.growing_selector, growing_tree.RANDOM)
    return growing_tree.gen(selector)

def main(args):
    g = grid.Grid(args.width, args.height);
    if args.quick:
        runner = silent_runner(not args.gui and not args.dest)
    elif args.gui:
        runner = gui_runner.GuiRunner(delay=args.wait, skulls=args.skulls, mark_path=args.mark_path, center_flood=args.center_flood)
    else:
        runner = print_runner

    commands = {
        'btree': btree.make,
        'sidewinder': sidewinder.make,
        'random_walk': random_walk.make,
        'random_adjacent': random_adjacent.make,
        'backtrack': backtrack.make,
        'wilson': wilson.make,
        'hunt_and_kill': hunt_and_kill.make,
        'growing_tree': gen_growing_tree(args)
    }
    command = commands.get(args.generator)
    kwargs = {}
    if args.speed:
        kwargs['delay'] = args.speed
    runner(command)(g, **kwargs)
    if args.mark_path:
        draw_longest_path(g, silent=(args.gui or args.dest))
    if args.center_flood:
        g.flood_center()
    if args.dest:
        write_file(args.dest, g)
    if args.stats:
        print "Deadends: %s" % (len(list(g.deadends())))

def run_main():
    parser = argparse.ArgumentParser(description='Generate Mazes.')
    parser.add_argument('generator', nargs='?',
                        choices=['wilson', 'btree', 'sidewinder', 'random_walk', 'random_adjacent', 'backtrack', 'hunt_and_kill', 'growing_tree'],
                        default='backtrack')
    parser.add_argument('-d', '--dest',
                        help='Specify a destination to write maze images to.')
    parser.add_argument('-x', '--stats', action='store_true',
                        help='Print stats after running the maze generator.')
    parser.add_argument('-s', '--speed', default='1', type=int,
                        help='Specify the speed of animation. Skip -S steps per frame.')
    parser.add_argument('-q', '--quick', action='store_true',
                        help='Disable all output until maze is generated')
    parser.add_argument('-g', '--gui', action='store_true')
    parser.add_argument('--width', default=20, type=int)
    parser.add_argument('--height', default=15, type=int)
    parser.add_argument('--mark-path', dest='mark_path', action='store_true')
    parser.add_argument('--center-flood', dest="center_flood", action='store_true')
    parser.add_argument('--growing-selector', nargs='?',
                        dest='growing_selector',
                        default='random',
                        choices=['random', 'first', 'last'])
    parser.add_argument('-w', '--gui-wait', dest='wait', default=0, type=int)
    parser.add_argument('--draw-skulls', help='draw sculls at deadends', action="store_true", dest="skulls")

    args = parser.parse_args()
    main(args)

if __name__ == "__main__":
    run_main()
