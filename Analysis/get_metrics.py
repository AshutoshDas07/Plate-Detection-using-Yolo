#!/usr/bin/python3

from similarity.cosine import Cosine
import matplotlib.pyplot as plt

def get_absolute_matches():
    f, g, ctr = open('model_res1.txt').readlines(), open('real_res').readlines(), 0
    for i in range(len(f)):
        if f[i] == g[i]:
            ctr += 1
        else:
            print(i+1, " ", f[i]," ", g[i])
    return ctr/len(f)

def get_similarity_score():
    cosine = Cosine(2)
    f, g, ctr = open('model_res1.txt').readlines(), open('real_res').readlines(), 0
    for i in range(len(f)):
        f[i], g[i] = f[i].replace("\n", ""), g[i].replace("\n", "")
        ctr += cosine.similarity_profiles(cosine.get_profile(f[i]), cosine.get_profile(g[i]))
    return ctr/len(f)


def get_license_confidence():
    f, ctr = open('avg_conf').readlines(), 0
    for val in f:
        val = val.replace("\n", "")
        ctr += float(val)
    return ctr/len(f)

def avg_letter_match():
    eight_letter , nine_letter, avg_letter, tot_letter, suffix, letter_match = 0, 0, 0, 0, 0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    f, g = open('model_res1.txt').readlines(), open('real_res').readlines()
    for i in range(len(f)):
        f[i], g[i] = f[i].replace("\n", ""), g[i].replace("\n","")
        if f[i] == g[i]:
            avg_letter += len(f[i])
            tot_letter += len(f[i])
            letter_match = [x+1 for x in letter_match]
        else:
            abs_letter = 0
            for j in range(min(len(f[i]),len(g[i]))):
                if f[i][j] == g[i][j]:
                    abs_letter += 1
                    letter_match[j] += 1
            avg_letter += abs_letter
            tot_letter += len(f[i])
            if (f[i].endswith(g[i]) or g[i].endswith(f[i])):
                suffix += 1
                continue
            if abs_letter == 8:
                eight_letter += 1
                continue
            if abs_letter == 9:
                nine_letter += 1
                continue

    return eight_letter/len(f), nine_letter/len(f), avg_letter/tot_letter, suffix/len(f), letter_match


if __name__ == '__main__':
    abs_match = get_absolute_matches()
    print("================================================\n \
          Absolute number of matches: ", abs_match)
    print("================================================\n \
          Similarity merit of matches: ", get_similarity_score())
    print("================================================\n \
          License Confidence: ", get_license_confidence())
    eight_letter_match, nine_letter_match, avg_match, suffix_match, letter_match = avg_letter_match()
    print("================================================\n \
          less than 8-letter matches: ", 1 - eight_letter_match - nine_letter_match - abs_match - suffix_match)
    print("================================================\n \
           Detections which are suffix: ", eight_letter_match)
    print("================================================\n \
          8-letter matches: ", eight_letter_match)
    print("================================================\n \
          9-letter matches: ", nine_letter_match)
    print("================================================\n \
          Average matched letters: ", avg_match)
    print("================================================\n \
          No of times each letter matched:", letter_match)
    fig, ax = plt.subplots(figsize=(10, 6))
    x_ax = [i+1 for i in range(10)]
    ax.bar(x_ax, letter_match, color='g')
    plt.xlabel('Position of letter')
    plt.ylabel('No of times letter matched')
    plt.savefig('Char_freq_plot.jpg')
