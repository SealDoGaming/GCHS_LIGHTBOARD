## Brady Has No Idea How To Make Actual HTML Code

And Thus he has to use the Github pages markdown to replicate it

However this does not give him the ability to do any of the things he wants to do.

<button id="test" onclick="change()">Click me</button>
<p>Music</p>
<div>
  <form>
    <input type="radio" id="music1" name="music" value="blocks.ogg">
    <label for="music1">Blocks</label><br>
    <input type="radio" id="music2" name="music" value="cantinaband60.wav">
    <label for="music2">Cantina Band</label><br>
    <input type="radio" id="music3" name="music" value="wilhemlscream.wav">
    <label for="music3">Wilhelm Scream</label>
  </form> 
</div>
<p>Pattern</p>
<div>
  <form>
    <input type="radio" id="pattern1" name="music" value="blocks.ogg">
    <label for="pattern1">Blocks</label><br>
    <input type="radio" id="pattern2" name="music" value="cantinaband60.wav">
    <label for="pattern2">Cantina Band</label><br>
  </form> 
</div>


<script>

  
  function change() {
  randomColor = Math.floor(Math.random()*16777215).toString(16);
  document.getElementById("test").style.backgroundColor = "#" + randomColor;
}
</script>

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/SealDoGaming/GCHS_LIGHTBOARD/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
