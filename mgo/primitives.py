
import numpy as np
import plotly.graph_objects as go
import mout

def point_trace(point,name=None):
	if not isinstance(point,list):
		point = [point]
	xs = [p[0] for p in point]
	ys = [p[1] for p in point]
	zs = [p[2] for p in point]
	return go.Scatter3d(name=name,x=xs,y=ys,z=zs,mode='markers')

def vector_trace(start,vec,name=None):
	return go.Scatter3d(name=name,x=[start[0],start[0]+vec[0]],y=[start[1],start[1]+vec[1]],z=[start[2],start[2]+vec[2]],mode='lines')

def sphere_data(centre,radius,samples=20):
	
	xs = []
	ys = []
	zs = []

	# polar then azimuth
	for polar in np.linspace(0,np.pi,samples):

		x_slice = []
		y_slice = []
		z_slice = []

		z = radius * np.cos(polar)
		r_xy = radius * np.sin(polar)

		for azimuth in np.linspace(0,2*np.pi,samples):

			x = r_xy * np.cos(azimuth)
			y = r_xy * np.sin(azimuth)

			x_slice.append(x + centre[0])
			y_slice.append(y + centre[1])
			z_slice.append(z + centre[2])

		x_slice += [x_slice[0],None]
		y_slice += [y_slice[0],None]
		z_slice += [z_slice[0],None]

		xs += x_slice
		ys += y_slice
		zs += z_slice

	# azimuth then polar
	for azimuth in np.linspace(0,2*np.pi,samples):

		x_slice = []
		y_slice = []
		z_slice = []

		for polar in np.linspace(0,np.pi,samples):

			z = radius * np.cos(polar)
			r_xy = radius * np.sin(polar)
			x = r_xy * np.cos(azimuth)
			y = r_xy * np.sin(azimuth)

			x_slice.append(x + centre[0])
			y_slice.append(y + centre[1])
			z_slice.append(z + centre[2])

		x_slice += [x_slice[0],None]
		y_slice += [y_slice[0],None]
		z_slice += [z_slice[0],None]

		xs += x_slice
		ys += y_slice
		zs += z_slice

	return xs, ys, zs

def sphere_trace(centre,radius,name=None,samples=20):

	xs, ys, zs = sphere_data(centre,radius,samples)

	return go.Scatter3d(x=xs,y=ys,z=zs,mode='lines')

def cone_trace(origin,target,radius,distance,name=None,samples=20,start_at_target=False,plot_caps=False,verbosity=1):
	r"""Cone trace for solid angle visualisation

	     O-----------
        / \         ^
       /   \        | D
	  /  T  \       | 
	 /|     |\      v
	/ |  X  | \------
	  |<--->|
	     R

	O: origin
	T: target 
	R: radius
	D: distance
	
	X: extended
	
	"""

	origin = np.array(origin)
	target = np.array(target)

	vec_origin_target = target - origin
	dist_origin_target = np.linalg.norm(vec_origin_target)
	unit_origin_target = vec_origin_target/dist_origin_target
	
	theta = np.arctan(radius/dist_origin_target)
	
	distance *= np.cos(theta)

	vec_origin_extended = distance * unit_origin_target
	extended = origin + vec_origin_extended

	if plot_caps and start_at_target:
		cap_radius = dist_origin_target * np.sin(theta)
		d_mod = dist_origin_target * np.cos(theta) * np.cos(theta)

	xs = []
	ys = []
	zs = []

	if plot_caps and start_at_target:

		if distance < dist_origin_target - cap_radius:
			if verbosity > 0:
				mout.warning('Skipping cone with distance < dist_origin_target')
			return go.Scatter3d(x=xs,y=ys,z=zs,mode='lines')

	else:
		if distance < dist_origin_target:
			if verbosity > 0:
				mout.warning('Skipping cone with distance < dist_origin_target')
			return go.Scatter3d(x=xs,y=ys,z=zs,mode='lines')

	#### DRAW THE CONE
	
	#### series of increasing circles along the extended vector origin --> target
	
	# orthogonal basis vectors for planes perpendicular to the cone's axis
	unit_vec_a = perpendicular_vector(vec_origin_target)
	unit_vec_a /= np.linalg.norm(unit_vec_a)
	unit_vec_b = np.cross(vec_origin_target,unit_vec_a)
	unit_vec_b /= np.linalg.norm(unit_vec_b)

	# define where to start drawing the cone
	if start_at_target:
		if plot_caps:
			start = d_mod
		else:
			start = dist_origin_target
	else:
		start = 0

	if start_at_target and dist_origin_target < distance:

		# draw the circles
		for i,d in enumerate(np.linspace(start,distance,samples)):
			if i == 0 and not start_at_target:
				continue				

			x_slice = []
			y_slice = []
			z_slice = []

			r = radius * d/dist_origin_target
			middle = origin + vec_origin_target/dist_origin_target * d
			
			for azimuth in np.linspace(0,2*np.pi,samples):

				point = unit_vec_a * np.sin(azimuth) + unit_vec_b * np.cos(azimuth)

				point *= r

				point += middle

				x = point[0]
				y = point[1]
				z = point[2]

				x_slice.append(x)
				y_slice.append(y)
				z_slice.append(z)

			if start_at_target and i == 0:
				first_x_slice = x_slice
				first_y_slice = y_slice
				first_z_slice = z_slice

			x_slice += [x_slice[0],None]
			y_slice += [y_slice[0],None]
			z_slice += [z_slice[0],None]

			xs += x_slice
			ys += y_slice
			zs += z_slice

			if i == samples - 1:

				# draw some lines along the outside of the cone

				if not start_at_target:

					for x,y,z in zip(x_slice[:-2],y_slice[:-2],z_slice[:-2]):

						xs.append(origin[0])
						xs.append(x)
						xs.append(None)
						
						ys.append(origin[1])
						ys.append(y)
						ys.append(None)

						zs.append(origin[2])
						zs.append(z)
						zs.append(None)

				else:

					for x1,y1,z1,x2,y2,z2 in zip(first_x_slice,first_y_slice,first_z_slice,x_slice[:-2],y_slice[:-2],z_slice[:-2]):

						xs.append(x1)
						xs.append(x2)
						xs.append(None)
						
						ys.append(y1)
						ys.append(y2)
						ys.append(None)
						
						zs.append(z1)
						zs.append(z2)
						zs.append(None)

	### DRAW THE CAP

	if plot_caps and start_at_target:

		cap_start = origin + (dist_origin_target - cap_radius) * unit_origin_target
		
		# polar then azimuth
		for i,polar in enumerate(np.linspace(0,np.pi/2-theta,samples//2)):
			if i == 0:
				continue
			if i == samples - 1:
				continue

			d = cap_radius* (1 - np.cos(polar))

			x_slice = []
			y_slice = []
			z_slice = []

			r = np.tan(polar) * (cap_radius - d)

			for azimuth in np.linspace(0,2*np.pi,samples):

				point = unit_vec_a * np.sin(azimuth) + unit_vec_b * np.cos(azimuth)

				point *= r

				point += cap_start + d * unit_origin_target

				x = point[0]
				y = point[1]
				z = point[2]

				x_slice.append(x)
				y_slice.append(y)
				z_slice.append(z)

			x_slice += [x_slice[0],None]
			y_slice += [y_slice[0],None]
			z_slice += [z_slice[0],None]

			xs += x_slice
			ys += y_slice
			zs += z_slice

		# azimuth then polar
		for azimuth in np.linspace(0,2*np.pi,samples):
			
			x_slice = []
			y_slice = []
			z_slice = []

			for i,polar in enumerate(np.linspace(0,np.pi/2-theta,samples//2)):
			
				d = cap_radius* (1 - np.cos(polar))

				r = np.tan(polar) * (cap_radius - d)

				point = unit_vec_a * np.sin(azimuth) + unit_vec_b * np.cos(azimuth)

				point *= r

				point += cap_start + d * unit_origin_target

				x = point[0]
				y = point[1]
				z = point[2]

				x_slice.append(x)
				y_slice.append(y)
				z_slice.append(z)

			x_slice.append(None)
			y_slice.append(None)
			z_slice.append(None)

			xs += x_slice
			ys += y_slice
			zs += z_slice
					
	return go.Scatter3d(name=name,x=xs,y=ys,z=zs,mode='lines')

def perpendicular_vector(v):
    if v[1] == 0 and v[2] == 0:
        if v[0] == 0:
            raise ValueError('zero vector')
        else:
            return np.cross(v, [0, 1, 0])
    return np.cross(v, [1, 0, 0])
