from textnode import TextNode, TextType


def main():
    test = TextNode('testing 1234', TextType.bold_text, 'https://www.example.com')
    print(repr(test))

if __name__ == "__main__":
    main()