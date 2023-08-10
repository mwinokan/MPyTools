
def sphere_trace(centre,radius,samples=20):

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

	return go.Scatter3d(x=xs,y=ys,z=zs,mode='lines')
