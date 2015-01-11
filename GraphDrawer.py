from nodebox.graphics import *
from helper_functions import *
import copy
from CographGenerator import CographGenerator

cograph = Graph()

def draw(canvas):
    canvas.clear()
    background(1)
    translate(500, 500)

    cograph.draw(weighted=False, directed=False)
    cograph.update(iterations=10)

def on_mouse_scroll(canvas, mouse):
    scale_num = 0
    for i in range(1, abs(mouse.scroll.y) + 1):
        scale_num += 1 / (float((i+2)*(i+2)))
    
    
    if mouse.scroll.y < 0:
        translate(mouse.x - mouse.x * (1 - scale_num) ,mouse.y - mouse.y * (1 - scale_num) )
        scale(1 - scale_num )

        for node in cograph.nodes:
            node.text.fontsize = (1 + scale_num * 1.2) * node.text.fontsize
    
    if mouse.scroll.y > 0:
        translate(mouse.x * (1 + scale_num) - mouse.x,mouse.y * (1 + scale_num) - mouse.y)
        
        scale(1 + scale_num )
        
        for node in cograph.nodes:
            node.text.fontsize = (1 - scale_num * 1.1) * node.text.fontsize
            
def on_key_press(canvas, keys):
    if keys.code == 'left':
        translate(1000, 0)
        
    if keys.code == 'right':
        translate(-1000, 0)
        
    if keys.code == 'down':
        translate(0, 1000)
        
    if keys.code == 'up':
        translate(0, -1000)
    
    if keys.code == 'f':
        canvas.fullscreen = not canvas.fullscreen 
        
def draw_graph(graph):
    global cograph
    cograph = graph
    canvas.fullscreen = True 
    canvas.on_mouse_scroll = on_mouse_scroll
    canvas.on_key_press = on_key_press

    for node in cograph.nodes:
        t = Text(node.id, fontsize=30)
        node.text = t
        node.radius = 100
        node.strokewidth = 100
    
    for edge in cograph.edges:
        color = Color(0,0,1)
        edge.stroke = color
    
    if len(cograph.nodes) > 15:
        cograph.distance = len(cograph.nodes) * len(cograph.nodes)
    else:
        cograph.distance = len(cograph.nodes) * 20

    canvas.run(draw)

if __name__ == '__main__':
    cotree = Tree("((((aaaaaaaaag,(aaaaaaaaah,aaaaaaaaai)0)0,(aaaaaaaaaj,aaaaaaaaak)1)1,(((aaaaaaaaal,(aaaaaaaaam,aaaaaaaaan)0)1,((aaaaaaaaao,aaaaaaaaap)0,((aaaaaaaaaq,aaaaaaaaar)0,(aaaaaaaaas,(aaaaaaaaat,aaaaaaaaau)1)1)1)0)1,(((aaaaaaaaav,aaaaaaaaaw)0,((aaaaaaaaax,aaaaaaaaay)0,((aaaaaaaaaz,aaaaaaaabb)1,((aaaaaaaabc,(aaaaaaaabd,aaaaaaaabe)1)0,((aaaaaaaabf,(aaaaaaaabg,aaaaaaaabh)0)0,(aaaaaaaabi,(aaaaaaaabj,aaaaaaaabk)0)0)0)0)1)0)1,(((aaaaaaaabl,aaaaaaaabm)1,((aaaaaaaabn,aaaaaaaabo)1,(aaaaaaaabp,aaaaaaaabq)1)0)0,(((aaaaaaaabr,(aaaaaaaabs,(aaaaaaaabt,(aaaaaaaabu,(aaaaaaaabv,aaaaaaaabw)1)1)0)1)0,((aaaaaaaabx,(aaaaaaaaby,(aaaaaaaabz,(aaaaaaaacc,(aaaaaaaacd,(aaaaaaaace,aaaaaaaacf)0)1)0)0)0)0,(aaaaaaaacg,aaaaaaaach)1)0)1,(((aaaaaaaaci,aaaaaaaacj)0,((aaaaaaaack,(aaaaaaaacl,(aaaaaaaacm,aaaaaaaacn)0)0)1,(aaaaaaaaco,(aaaaaaaacp,(aaaaaaaacq,(aaaaaaaacr,(aaaaaaaacs,aaaaaaaact)0)1)1)1)0)0)1,(((aaaaaaaacu,(aaaaaaaacv,aaaaaaaacw)0)1,((aaaaaaaacx,aaaaaaaacy)1,(aaaaaaaacz,aaaaaaaadd)0)1)0,((aaaaaaaade,(aaaaaaaadf,(aaaaaaaadg,(aaaaaaaadh,aaaaaaaadi)1)1)0)0,((aaaaaaaadj,aaaaaaaadk)0,(aaaaaaaadl,(aaaaaaaadm,(aaaaaaaadn,aaaaaaaado)1)0)0)1)1)1)0)0)0)1)0)1,(((aaaaaaaadp,aaaaaaaadq)1,((aaaaaaaadr,aaaaaaaads)0,((aaaaaaaadt,aaaaaaaadu)1,((aaaaaaaadv,aaaaaaaadw)0,(aaaaaaaadx,(aaaaaaaady,aaaaaaaadz)0)1)1)0)1)0,(((aaaaaaaaee,aaaaaaaaef)0,aaaaaaaaaa)1,((aaaaaaaaab,aaaaaaaaac)0,(aaaaaaaaad,(aaaaaaaaae,aaaaaaaaaf)0)1)0)1)0);",format=8)
    cotree.name = '1'
    generator = CographGenerator()
    print cotree
    cograph = generator.generate_cograph_from_cotree(cotree)
#     cograph = Graph()
#           
#     cograph.add_edge('a', 'c')
#     cograph.add_edge('b', 'e')
#     cograph.add_edge('c', 'd')
#     cograph.add_edge('d', 'a')
#     cograph.add_edge('d', 'b')
#     cograph.add_edge('d', 'c')
#     cograph.add_edge('e', 'c')
#     
#     cograph = get_complement(cograph)
    
    draw_graph(cograph)

