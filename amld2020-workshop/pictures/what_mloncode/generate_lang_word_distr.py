import os

from matplotlib import pyplot as plt

wiki_link = "https://en.wikipedia.org/wiki/List_of_dictionaries_by_number_of_words"

root = "../why_mloncode_hard/langs/"

cnts = [49 * 10 ** 6]
languages = ["Source Code Identifiers"]

# cnts = []
# languages = []

data_to_use = """Korean	1,100,373
Turkish	616,767
Japanese	500,000
English	470,000
Russian	150,000
"""


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


for line in data_to_use.splitlines():
    words = line.strip().split()
    if len(words) == 2:
        print(" ".join(words))
        cnts.append(int(words[1].replace(",", "")))
        languages.append(words[0])

languages = list(reversed(languages))
cnts = list(reversed(cnts))


def plot_hist(langs, cnts, transparent_since=-1):
    return plt.barh(y=range(len(cnts)), width=cnts, tick_label=[""] * len(cnts),
                    height=.9999, fc=(1, 0, 0, 0.5), edgecolor='black', hatch="/")


def autolabel(rects, ax, bar_labels, transparent_since=-1, show_last=False):
    # import pdb;pdb.set_trace()
    x_step = max(rect.get_width() for rect in rects) * 0.1
    for idx, rect in enumerate(rects):
        height = rect.get_height()
        rect_text = bar_labels[idx]
        if idx < transparent_since:
            rect_text += " " + human_format(rect.get_width())
        ax.text(rect.get_x() + x_step, rect.get_y() + .5 * height,
                rect_text,
                ha='left', va='center', rotation=0, weight='bold', fontsize=38)

        if idx >= transparent_since:
            rect.set_alpha(0)
            continue
        rect.set_linewidth(10)

        " + rect.get_width() / 2."
        print(rect.get_width(), rect.get_x())
    if show_last:
        rect_text = bar_labels[-1]
        rect_text += " " + human_format(rects[-1].get_width())
        height = rects[-1].get_height()
        ax.text(rects[-1].get_x() + x_step, rects[-1].get_y() + .5 * height,
                rect_text,
                ha='left', va='center', rotation=0, weight='bold', fontsize=38)
        rects[-1].set_linewidth(10)


def plot_pipeline(langs, cnts):
    # plt.ion()
    for i in range(len(cnts)):
        tmp_langs = [l for l in langs[:i + 1]]
        tmp_cnts = [c for c in cnts[:i + 1]]
        max_v = tmp_cnts[-1]

        for _ in range(len(cnts) - i - 1):
            tmp_langs.append("")
            tmp_cnts.append(max_v * 2)

        fig, ax = plt.subplots()
        fig.set_size_inches(12, 12)
        bar_plot = plot_hist(langs=tmp_langs, cnts=tmp_cnts, transparent_since=i)

        autolabel(rects=bar_plot, ax=ax, bar_labels=tmp_langs, transparent_since=i)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        plt.show(block=False)
        plt.savefig(os.path.join(root, "langs_%s.png" % i))
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 12)
    bar_plot = plot_hist(langs=langs, cnts=cnts, transparent_since=len(cnts))

    autolabel(rects=bar_plot, ax=ax, bar_labels=langs, transparent_since=len(cnts), show_last=True)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    plt.show(block=False)
    plt.savefig(os.path.join(root, "langs_%s.png" % len(cnts)))
    plt.show()


plot_pipeline(langs=languages, cnts=cnts)

# fig, ax = plt.subplots()
# "tick_label=languages, log=True"
# bar_plot = plt.barh(y=range(len(cnts)), width=cnts, tick_label=[""] * len(cnts),
#                     height=.9999, fc=(1, 0, 0, 0.5),  edgecolor='black', hatch="/")
#
#
#
#
# autolabel(rects=bar_plot, ax=ax, bar_labels=languages)
# plt.show()

def generate_bool_combinations(length=3):
    if length == 0:
        yield []
        return
    for v in [True, False]:
        for r in generate_bool_combinations(length=length - 1):
            yield [v] + r

































