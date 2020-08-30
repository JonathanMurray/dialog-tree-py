from typing import Callable, Iterator


def layout_text_in_area(text: str, font_width: Callable[[str], int], width: int) -> Iterator[str]:
    if len(text) == 0:
        yield ""
        return

    start = 0
    end = 0
    while True:

        if text[start] == ' ':
            # Our line is starting with whitespace --> advance forward to skip whitespace
            for i in range(start + 1, len(text) + 1):
                if text[i] != ' ':
                    start = i
                    break

        if end >= len(text):
            # We have reached the end of the string --> we're done
            yield text[start:]
            return
        substr = text[start:end + 1]
        overflow = font_width(substr) > width
        if overflow:
            # we have a substring [start->end] that is wider than allowed
            if text[end] == ' ':
                # we are at a word-boundary so we can return all previous text
                yield text[start:end]
                start = end
            else:
                # mid-word --> we need to go back left to find a word-boundary to wrap line at
                found = False
                for i in range(end - 1, start, -1):
                    if text[i] == ' ':
                        # we found a word boundary --> yield line and go on with main loop
                        yield text[start:i + 1]
                        start = end = i + 1
                        found = True
                        break
                if not found:
                    # failed to find a word-boundary --> resort to returning mid-word
                    yield text[start:end]
                    start = end
        else:
            end += 1
