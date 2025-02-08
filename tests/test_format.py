from doctestcase import DocTestCase


class TitleDepth(DocTestCase):
    """
    Title
    """

    def test_title_depth(self):
        for i in range(1, 8):
            self.assertEqual(
                '{} Title\n'.format('#' * i),
                self.to_markdown(title_depth=i),
            )

    def test_title_char(self):
        for c in '=-^"':
            self.assertEqual(
                'Title\n{}\n'.format(c * len('Title')),
                self.to_rest(title_char=c),
            )
