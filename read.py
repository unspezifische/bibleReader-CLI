import sys
from rich.console import Console

import xml.etree.ElementTree as ET

console = Console()

# Get the book abbreviation and chapter number from command line arguments
if len(sys.argv) < 3:
    print("Usage: python3 usx.py <book_abbreviation> [chapter_number] <version> ")
    sys.exit(1)

book_abbreviation = sys.argv[1].upper()

# Check if a specific chapter number is provided
if len(sys.argv) >= 4:
    # if a chapter is provided, then version is the last argument
    chapter_number = sys.argv[2]
    version = sys.argv[3].upper()
elif len(sys.argv) == 3:
    # if no chapter is provided, then version is the last argument
    version = sys.argv[2].upper()
    chapter_number = None

filename = f'Versions/{version}/{book_abbreviation}.usx'

tree = ET.parse(filename)

chapter_num = None
process_nodes = False

for node in tree.iter():
    if node.tag == 'chapter':
        if node.get('number') == chapter_number:
            console.print(f"[bold]Chapter {chapter_number} [bold]", justify='center')
            process_nodes = True
        elif node.get('sid') and process_nodes:
            process_nodes = False

    if process_nodes and node.tag != 'chapter':
        # console.print("Node:", ET.tostring(node).decode())
        style = node.get('style')

        if node.tag == 'para':
            # Perform actions based on the style of the node
            if style == 'h':
                book = node.text
                console.print("[bold]" + book + "[bold]", justify='center', end="")
                
            elif style == 'toc1':
                continue
            elif style == 'toc2':
                continue
            elif style == 'toc3':
                continue
            elif style == 'mt1':
                continue
                
            elif style == 'mr':
                console.print("Margin paragraph", end="")
            elif style == 's1':
                console.print()
                console.print("[bold]" + node.text + "[bold]", justify='center', end="")

            elif style == 's2':
                console.print("Minor section heading", end="")
            elif style == 'sr':
                console.print("Section reference range", end="")
            
            elif style == 'r':
                ## We can skip this <para> because the child node gets processed and rendered
                # console.print("Reference:", ET.tostring(child).decode())
                continue
                
            elif style == 'd':
                console.print("Descriptive title", end="")
            elif style == 'sp':
                console.print("Speaker identification", end="")

            elif style == 'p':
                console.print("    ", end="")
            elif style == 'm':
                console.print("    ", end="") ## When starting a new paragraph, console.print a new line and return to the left margin.

            elif style == 'pmo':
                console.print("Embedded text opening", end="")
            elif style == 'pm':
                console.print("Embedded text paragraph", end="")
            elif style == 'pmc':
                console.print("Embedded text closing")
            elif style == 'pmr':
                console.print("Embedded text refrain", end="")
            elif style == 'pi1':
                console.print("Indented paragraph.", end="")

            elif style == 'mi':
                console.print("Indented flush left paragraph", end="")
            elif style == 'cls':
                console.print("Closure of an epistle / letter", end="")

            elif style == 'li1':
                console.print("List item (out-dented paragraph meant to highlight the items of a list.)", end="")

            elif style == 'pc':
                console.print("Centered paragraph", end="")

            elif style == 'lit':
                console.print("Liturgical note/comment", end="")
            
            elif style == 'q1':
                ## q1 is a non-indented poetic line
                console.print("[italic]" + node.text + "[/italic]", end="")
            elif style == 'q2':
                ## q2 is indented poetic line
                console.print("[italic]    " + node.text + "[/italic]", end="")
            elif style == 'qr':
                ## qr is right-justifyed poetic line
                console.print("[italic]" + node.text + "[/italic]", justify='right', end="")
            elif style == 'qc':
                console.print("[italic]" + node.text + "[/italic]", justify='center', end="")
            elif style == 'qa':
                console.print("Acrostic heading", end="")
            elif style == 'qm1':
                console.print("Embedded text poetic line", end="")
                # console.print("# represents the level of indent (i.e. qm1, qm2, etc.)")

            elif style == 'b':
                console.print("**")   ## console.print a blank line when explicitly told to do so.
            else:
                console.print("Unknown style:", style)

            for child in node:
                if child.tag == 'verse':
                    if child.get('eid'):
                        continue    ## Skip this node because it is useless

                    if child.get('number'):
                        console.print(f"{child.get('number')}", end=" ")
                    if child.tail:
                        if node.get('style') == 'q1':
                            console.print("[italic]" + child.tail + "[/italic]", end="")
                        else:
                            console.print(child.tail, end="")
                            
                elif child.tag == 'note':
                    console.print(f"[magenta]{child.get('caller')}[/magenta]", end="")
                    if child.tail:
                        console.print(child.tail, end="")

            if style != 'b':
                console.print('-----------------')


        elif node.tag == 'ref':
            console.print(f"({node.text})", justify='center')


        elif node.tag == 'char':
            if node.tag == 'ft' or node.tag == 'ft':
                console.print("Text:", node.text)
                console.print("Tail:", node.tail)
                continue    ## Skip these nodes because they are processed in the 'note' block

            elif node.tag == 'ior':
                console.print("Introduction outline reference range.")
                console.print("An introduction outline entry typically ends with a range of references, sometimes within parentheses. This is an optional char style for marking these references separately.")
                console.print("Valid in: Book Introduction")

            elif node.tag == 'iqt':
                console.print("Introduction quoted text.")
                console.print("Scripture quotations, or other quoted text, appearing in the Book Introduction.")
                console.print("Valid in: Book Introduction")

            elif node.tag == 'add':
                console.print("Translator’s addition.")
                console.print("Words added by the translator for clarity – text which is not literally a part of the original language, but which was supplied to make the meaning of the original clear.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'bk':
                console.print("Quoted book title.")
                console.print("Often italized, this is a book title that is quoted in the text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'dc':
                console.print("Deuterocanonical/LXX additions or insertions in the Protocanonical text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'k':
                console.print("Keyword / keyterm.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'nd':
                console.print("Name of God (name of deity).")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'ord':
                console.print("Ordinal number ending")
                console.print('i.e. in 1st — 1<char style="ord">st</char>')
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'pn':
                console.print("Proper name.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'qac':
                console.print("Used to indicate the acrostic letter within a poetic line.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'qs':
                console.print("qs tag")
                console.print('Used for the expression "Selah” commonly found in Psalms and Habakkuk.\nThis text is frequently right justifyed, and rendered on the same line as the previous poetic text, if space allows.')
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'qt':
                console.print("Quoted text.")
                console.print("Old Testament quotations in the New Testament, or other quotations")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'rq':
                console.print("Inline quotation reference(s).")
                console.print("A reference indicating the source text for the preceding quotation (usually an Old Testament quote).\nThe reference(s) are intended to be formatted within the scripture body text column, and not extracted from the text as are regular cross-references. They are also typically separated from the main text of Scripture using a different type style and justifyment.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'sig':
                console.print("Signature of the author of an epistle.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'sls':
                console.print("sls tag")
                console.print("Passage of text based on a secondary language or alternate text source.\nFor example: The Nouvelle Bible Segond 2002 (NBS02) has large sections of text in EZR and DAN in italics, to represent where the original text is in Aramaic, not Hebrew.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'tl':
                console.print("tl tag")
                console.print("Transliterated (or foreign) word(s).")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'wj':
                console.print("wj tag")
                console.print("Words of Jesus.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'bd':
                console.print("bd tag")
                console.print("Bold text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'bdit':
                console.print("bdit tag")
                console.print("Bold italic text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'em':
                console.print("em tag")
                console.print("Emphasized text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'it':
                console.print("it tag")
                console.print("Italic text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'no':
                console.print("no tag")
                console.print("Superscript ordinal number.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'sc':
                console.print("sc tag")
                console.print("Small caps text.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'pro':
                console.print("Pronunciation information")
                console.print("Used for CJK texts.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'w':
                console.print("WWordlist/glossary/dictionary entry.")
                console.print("Surround word(s) with this char style to indicate that it appears (or should appear) in a published word list/glossary.")
                console.print("Valid in: Any valid <char>")

            elif node.tag == 'wg':
                console.print("Greek word list entry.")

            elif node.tag == 'wh':
                console.print("Hebrew word list entry.")

        elif node.tag == 'note' or node.tag == 'verse':
            continue    ## Skip these nodes because they are processed in the 'para' block

        else:
            console.print("^^^^^^^^^^^")   ## console.print a blank line before console.printing the unknown tag
            console.print("-*-*-*-*-*-")
            console.print("Unknown tag:", node.tag)
            console.print("Node:", ET.tostring(node).decode())
            console.print("-*-*-*-*-*-")
