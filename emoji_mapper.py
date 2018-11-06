import emoji
import re
import csv
        
tweet_file = "data/all_emoji_tweets_02_11_18_sorted_3.csv"
emoji_mappings_file = "data/emoji_mapping.csv"

def split_count(text):

    emoji_list = []
    data = re.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list

def get_emoji_mappings(emoji_mappings_file):
    emoji_mappings = {}
    print("open")
    with open(emoji_mappings_file, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            for emoji in row[0].split(','):
                try:
                    if(int(row[1]) > 0):
                        emoji_mappings[emoji] = row[0]
                except:
                    emoji_mappings[emoji] = row[1]
    return emoji_mappings


def map_emojis_in_tweets(tweet_file, emoji_mappings_file):
    emoji_cnt = {}
    emoji_mappings = get_emoji_mappings(emoji_mappings_file)
    with open(tweet_file, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
            #print(', '.join(row))

            counter = split_count(row[1])
            unique_counter = {}
            for emoji in counter:
                unique_counter[emoji_mappings[emoji]]=1
                #unique_counter[emoji] = 1
            for emoji in unique_counter:
                if emoji not in emoji_cnt:
                    emoji_cnt[emoji] = 0
                emoji_cnt[emoji] += 1

            '''
            i += 1
            if i > 100:
                break;
            '''
    return emoji_cnt
    
def sort_emoji_count_by_value(emoji_cnt):
    sorted_by_value = sorted(emoji_cnt.items(), key=lambda kv: kv[1])
    sorted_by_value.reverse()
    return sorted_by_value
    
def display_emoji_count(emoji_cnt):
    for emoji_tuple in emoji_cnt:
        print(emoji_tuple[0]+": "+str(emoji_tuple[1]))

def write_emoji_count(emoji_cnt, emoji_cnt_file):
    with open(emoji_cnt_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', 
                            quoting=csv.QUOTE_MINIMAL)
        #writer.writeheader()
        writer.writerows(emoji_cnt)

#if __name__ == 'main':
mappings = get_emoji_mappings(emoji_mappings_file)
print(mappings)
    #emoji_cnt = map_emojis_in_tweets(tweet_file, emoji_mappings_file)
    #emoji_cnt = sort_emoji_count_by_value(emoji_cnt)
#display_emoji_count(emoji_cnt)