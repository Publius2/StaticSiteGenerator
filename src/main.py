from textnode import TextNode, TextType


def main():
    test = TextNode('testing 1234', TextType.Bold_text, 'https://www.example.com')
    print(test)

if __name__ == "__main__":
    main()