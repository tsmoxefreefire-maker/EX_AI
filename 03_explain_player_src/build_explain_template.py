import os, sys
d=os.path.dirname(os.path.abspath(__file__))+os.sep   # the sources live next to this script
s=open(d+"explain.js",encoding="utf-8").read().replace("/*WORLD*/","",1)
w=open(d+"world.js",encoding="utf-8").read();nr=open(d+"narrator.js",encoding="utf-8").read()
if "function sceneWorld(" not in s: s=s.replace("let current=null;","let current=null;\n"+w,1)
if "THE NARRATOR + VIDEO MODE" not in s: s=s.replace("let current=null;","let current=null;\n"+nr,1)
pl=open(d+"play.js",encoding="utf-8").read()
if "THE FILM ENGINE" not in s: s=s.replace("let current=null;","let current=null;\n"+pl,1)
ms=open(d+"more_scenes.js",encoding="utf-8").read()
if "interview · 🎴 flip" not in s: s=s.replace("let current=null;","let current=null;\n"+ms,1)
ms2=open(d+"more_scenes2.js",encoding="utf-8").read()
if "build · 🗣️ talk" not in s: s=s.replace("let current=null;","let current=null;\n"+ms2,1)
st=open(d+"art_secondary.js",encoding="utf-8").read()+"\n"+open(d+"art_more.js",encoding="utf-8").read()+"\n"+open(d+"lego.js",encoding="utf-8").read()+"\n"+open(d+"stage.js",encoding="utf-8").read()   # 📐 art for the big grades + 👥 the age stages
if "THE AGE STAGES" not in s: s=s.replace("let current=null;","let current=null;\n"+st,1)
n5=open(d+"sound.js",encoding="utf-8").read()+"\n"+open(d+"more_scenes3.js",encoding="utf-8").read()   # 🎵 the sounds + 🆕 the 5 new activities (batch 26)
if "five new activities" not in s: s=s.replace("let current=null;","let current=null;\n"+n5,1)
shell=open(d+"explain_shell.html",encoding="utf-8").read()
css="".join(open(d+f,encoding="utf-8").read() for f in ["part2_games.css","new_css.css","alive.css","more.css","chars.css","order.css","throw.css","art.css","batch10.css","predict.css","explain_w.css","narrator.css","play.css","more.css2","more.css3","polish.css","stage.css","acts.css"])
js=open(d+"part3_core.js",encoding="utf-8").read()+"\n"+s+"\n})();\n"
open(sys.argv[1] if len(sys.argv)>1 else os.path.join(d,"..","02_question_factory","player","explain_template.html"),"w",encoding="utf-8").write(shell.replace("</head>",css+"</head>",1).replace("/*JS*/",js))
print("explain template built")
