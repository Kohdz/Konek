// let total = 90;
let systems;
let gravity;
let repeller;
let wh = window.innerHeight

if  (wh <= 640){
  total = 15
} else if (wh <= 1024) {
  total = 55
} else {
  total = 70
}




function setup() {


  canvas = createCanvas(windowWidth,windowHeight);
  canvas.position(0,0)
  canvas.style('z-index', '-1')
  canvas.style('left', '-1%')

  systems = [];
  for(let i =0;i<total;i++){
    systems.push(new Particle(createVector(floor(random(width)),floor(random(height)))));
  }

}


function draw() {
  
  background('rgb(0,0,0, 0)'); //background(51)
  for(let i=0;i<systems.length;i++){
    systems[i].show();

    for(let j=0;j<systems.length;j++){
      let distance = dist(systems[i].location.x,systems[i].location.y,systems[j].location.x,systems[j].location.y);
      strokeWeight(.9);

      if(distance<200){
        let lineAlpha = map(distance,0,200,255,0);
        stroke(0, 0, 0, lineAlpha); //stroke(255,255,255,lineAlpha);
        line(systems[i].location.x,systems[i].location.y,systems[j].location.x,systems[j].location.y);

      }

    }
    systems[i].update();
  }

}
function mousePressed(){
  systems.push(new Particle(createVector(mouseX,mouseY)));
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight)
}

