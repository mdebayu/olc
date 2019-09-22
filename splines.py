import pygame
import numpy as np


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,153)

screen_size = (700, 500)
pt_size = 5
mgn = 3

def CatmullRomSpline(P0, P1, P2, P3, nPoints=1000):
  """
  P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
  nPoints is the number of points to include in this curve segment.
  """
  # Convert the points to numpy so that we can do array multiplication
  P0, P1, P2, P3 = map(np.array, [P0, P1, P2, P3])

  # Calculate t0 to t4
  alpha = 0.5

  def tj(ti, Pi, Pj):
    xi, yi = Pi
    xj, yj = Pj
    return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

  t0 = 0
  t1 = tj(t0, P0, P1)
  t2 = tj(t1, P1, P2)
  t3 = tj(t2, P2, P3)

  # Only calculate points between P1 and P2
  t = np.linspace(t1,t2,nPoints)

  # Reshape so that we can multiply by the points P0 to P3
  # and get a point for each value of t.
  t = t.reshape(len(t),1)
  A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
  A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
  A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3
  B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
  B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

  C  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
  return C

def CatmullRomChain(P):
  """
  Calculate Catmull Rom for a chain of points and return the combined curve.
  """
  sz = len(P)
  # The curve C will contain an array of (x,y) points.
  C = []
  for i in range(sz-3):
    c = CatmullRomSpline(P[i], P[i+1], P[i+2], P[i+3])
    C.extend(c)

  return C

def CatmullRomCircle(P):
  sz = len(P);

  C = []
  for i in range(sz):
    c = CatmullRomSpline(P[i], P[(i+1)%sz], P[(i+2)%sz], P[(i+3)%sz])
    C.extend(c)
  return C


def draw_hltpt(screen,pt,hlt=BLACK):
	highlight = [pt[0]-mgn,pt[1]-mgn, pt[2]+2*mgn, pt[3]+2*mgn]
	if hlt!= BLACK:
		pygame.draw.rect(screen,hlt,highlight)
	pygame.draw.rect(screen,WHITE,pt)

def get_points(num_pts,crv_type):
	pts = [];
	if crv_type == "STRAIGHT":
		for i in range(num_pts):
			pts.append([((i+1)*screen_size[0])/(num_pts+1), screen_size[1]/2, pt_size, pt_size])
	if crv_type == "CIRCLE" or crv_type == "IRREGULAR":
		for i in range(num_pts):
			x = (screen_size[0]/4) * np.cos(i*np.pi*2/num_pts) + (screen_size[0]/2)
			y = (screen_size[1]/4) * np.sin(i*np.pi*2/num_pts) + (screen_size[1]/2)
			
			if crv_type == "IRREGULAR":
				x+= (np.random.rand() - 0.5) * (screen_size[0]/8)
				y+= (np.random.rand() - 0.5) * (screen_size[1]/8)

			pts.append([x,y,pt_size,pt_size])

	return pts

def main():
	pygame.init()
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption("Splines")
	clock = pygame.time.Clock()

	pygame.key.set_repeat(1)
	
	quit = False

	crv_types = ["IRREGULAR","CIRCLE","STRAIGHT"]
	crv = 0

	while not quit:
		pts = get_points(20,crv_types[crv])
		sel_pt = 0
		reset = False
		while not reset and not quit:
			move = [0,0]; STEPS = 5;

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit = True
				if event.type == pygame.KEYDOWN:
					if pygame.key.get_pressed()[pygame.K_ESCAPE]:
						quit = True
					if pygame.key.get_pressed()[pygame.K_UP]:
						move = [0,-STEPS]
					if pygame.key.get_pressed()[pygame.K_RIGHT]:
						move = [STEPS,0]
					if pygame.key.get_pressed()[pygame.K_DOWN]:
						move = [0,STEPS]
					if pygame.key.get_pressed()[pygame.K_LEFT]:
						move = [-STEPS,0]
					if pygame.key.get_pressed()[pygame.K_z]:
						sel_pt += 1
						if sel_pt > len(pts)-1:
							sel_pt = 0
					if pygame.key.get_pressed()[pygame.K_x]:
						sel_pt -= 1
						if sel_pt <0:
							sel_pt = len(pts)-1

					if pygame.key.get_pressed()[pygame.K_SPACE]:
						reset = True

					if pygame.key.get_pressed()[pygame.K_TAB]:
						crv += 1
						crv = crv%len(crv_types) 
						reset = True

				pts[sel_pt][0] += move [0]
				pts[sel_pt][1] += move [1]
			P=[]
			for p in pts:
				P.append([p[0],p[1]])

			C = CatmullRomCircle(P)

			# Draw the points and curves
			screen.fill(BLACK)

			for i,pt in enumerate(pts):
				if i != sel_pt:
					draw_hltpt(screen,pt,YELLOW)
				else:
					draw_hltpt(screen,pt,RED)
			for p in C:
				draw_hltpt(screen,[p[0],p[1],1,1], BLACK)
			

			pygame.display.flip()
			clock.tick(60);

if __name__ == "__main__":
	main() 