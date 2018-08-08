from collections import deque
import queue

EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
WORDLIST = "/Users/jtimarnold/Downloads/SVNDigger/all.txt"

print(f'my name is {__name__}')

def get_words():
    
    def extend_words(word):
        if "." in word:
            words.put(f'/{word}')
        else:
            words.put(f'/{word}/')

        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')
    
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = queue.Queue()
    for word in raw_words.split():
        extend_words(word)
            
    return words

def main():
    print('see how that\'s different?')

if __name__ == '__main__':
    main()


<<<<<<< HEAD
=======


>>>>>>> upstream/master
try:
    do_something()
except (IOError):
    print('something IO happened')
<<<<<<< HEAD
except AttributeError:
=======
except AttributError:
>>>>>>> upstream/master
    print('something attr happened')
else:
    print('good')
finally:
<<<<<<< HEAD
    print('cleanup')
=======
    print('cleanup')

>>>>>>> upstream/master
