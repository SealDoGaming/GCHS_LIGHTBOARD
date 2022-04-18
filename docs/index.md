## Brady Has No Idea How To Make Actual HTML Code

And Thus he has to use the Github pages markdown to replicate it

However this does not give him the ability to do any of the things he wants to do.

<button id="test" onclick="change()">Click me</button>
<button id="boost" onclick="upValue()">Dash Boost</button>


<script>
  import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.6.10/firebase-app.js;
  import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/9.6.10/firebase-firestore.js';
  const firebaseConfig = {

    apiKey: "AIzaSyB9xPGyQgptYXqQ7eeoE7HJ48YAVkJJBW0",

    authDomain: "gchs-lightboard.firebaseapp.com",

    databaseURL: "https://gchs-lightboard-default-rtdb.firebaseio.com",

    projectId: "gchs-lightboard",

    storageBucket: "gchs-lightboard.appspot.com",

    messagingSenderId: "68756304353",

    appId: "1:68756304353:web:98dd2137e81bf73e8da2a0",

    measurementId: "G-TGRSFPT64W"

  };
  


  const app = initializeApp(firebaseConfig);
  const db = firebase.firestore();
  const increment = firebase.firestore.FieldValue.increment(1);
  const speedyDash = db.collection('light_patterns_votes').doc('Speedy_Dash.pickle');

  

  
  function change() {
  var randomColor = Math.floor(Math.random()*16777215).toString(16);
  document.getElementById("test").style.backgroundColor = "#" + randomColor;
}
  function upValue() {
    speedyDash.update({ votes: increment });
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
