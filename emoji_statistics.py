import emoji
import regex
import csv
        
tweet_file = "data/german_tweets_text_id_only_387627_samples.csv"
emoji_cnt_file = "data/emoji_cnt_from_387627_samples.csv"

def split_count(text):

    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list


def count_emojis_in_tweets(tweet_file):
    emoji_cnt = {}
    with open(tweet_file, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
            #print(', '.join(row))
            line = [row[1]]
        
            counter = split_count(line[0])
            unique_counter = {}
            for emoji in counter:
                unique_counter[emoji] = 1 
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

emoji_cnt = count_emojis_in_tweets(tweet_file)
emoji_cnt = sort_emoji_count_by_value(emoji_cnt)

write_emoji_count(emoji_cnt, emoji_cnt_file)
#display_emoji_count(emoji_cnt)