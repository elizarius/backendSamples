class Palindrome:

    @staticmethod
    def is_palindrome(word):
        ls = len(word)
        for i in range(0,ls):
            print("AELZ letter {}".format(word[i]))
            if word[i].lower() != word[ls-i-1].lower():
                return False
        
        return True

print(Palindrome.is_palindrome('Deleveled'))
