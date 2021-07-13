import numpy as np
import math

# Space Mission Analysis and Design ed.3 p.897 : a
earth_equatorial_radius = 6378.13649
# Space Mission Analysis and Design ed.3 p.897 : b or c
earth_polar_radius = 6356.7517
# Space Mission Analysis and Design ed.3 p.897 : (a**2 * c)^(1/3)
earth_mean_radius = (earth_equatorial_radius ** 2 * earth_polar_radius) ** (1 / 3)

# Space Mission Analysis and Design ed.3 p. 900 : f = (a-b)/a
earth_flattening = (earth_equatorial_radius - earth_polar_radius) / earth_equatorial_radius

# Space Mission Analysis and Design ed.3 p. 900 : e = (2*f - f**2)**(1/2) = ((a**2 - b**2)**(1/2))/a
earth_ellipsoidal_eccentricity = (2 * earth_flattening - earth_flattening ** 2) ** (1 / 2)


def convert_geocentric_coord_to_x_y_z(phi_p, lambda_, r, degrees=True):
	"""
	Source : Space Mission Analysis and Design ed.3 p.900

	Args:
		degrees:
		phi_p : latitude
		lambda_ : longitude
		r : distance from earth center

	Returns:
		X
		Y
		Z
	"""

	if degrees:
		phi_p = np.deg2rad(phi_p)
		lambda_ = np.deg2rad(lambda_)

	X = r * (np.cos(phi_p) * np.cos(lambda_))
	Y = r * (np.cos(phi_p) * np.sin(lambda_))
	Z = r * np.sin(phi_p)

	return X, Y, Z


def convert_x_y_z_to_geocentric_coord(X, Y, Z):
	"""
	Source : Space Mission Analysis and Design ed.3 p.900

	Args:
		X
		Y
		Z

	Returns:
		phi_p : latitude
		lambda_ : longitude
		r : distance from earth center
	"""

	phi_p = np.arctan(Z / ((X ** 2 + Y ** 2) ** (1 / 2)))
	lambda_ = np.arctan2(Y, X)
	r = (X ** 2 + Y ** 2 + Z ** 2) ** (1 / 2)

	return np.rad2deg(phi_p), np.rad2deg(lambda_), r


def convert_geodetic_coord_to_x_y_z(phi, lambda_, h, degrees=True):
	"""
	Source : Space Mission Analysis and Design ed.3 p.900

	Args:
		degrees:
		phi : latitude
		lambda_ : longitude
		h : altitude

	Returns:
		X
		Y
		Z
	"""

	a = earth_equatorial_radius
	b = earth_polar_radius

	e = (a ** 2 - b ** 2) ** (1 / 2) / a

	if degrees:
		phi = np.deg2rad(phi)
		lambda_ = np.deg2rad(lambda_)

	N = a / ((1 - e ** 2 * np.sin(phi) ** 2) ** (1 / 2))
	X = (N + h) * np.cos(phi) * np.cos(lambda_)
	Y = (N + h) * np.cos(phi) * np.sin(lambda_)
	Z = ((1 - e ** 2) * N + h) * np.sin(phi)

	return X, Y, Z


def convert_x_y_z_to_geodetic_coord(X, Y, Z):
	"""
	Source : Space Mission Analysis and Design ed.3 p.900

	Args:
		X
		Y
		Z

	Returns:
		phi_p : latitude
		lambd : longitude
		h : altitude
	"""

	a = earth_equatorial_radius
	b = earth_polar_radius

	# Error if Z is negative so will keep the sign and the value separately
	z = np.abs(Z)
	z_sign = Z / z

	R = (X ** 2 + Y ** 2) ** (1 / 2)
	E = (b * z - (a ** 2 - b ** 2)) / (a * R)
	F = (b * z + (a ** 2 - b ** 2)) / (a * R)
	P = 4 * (E * F + 1) / 3
	Q = 2 * (E ** 2 - F ** 2)
	D = (P ** 3 + Q ** 2) ** (1 / 2)
	v = (D - Q) ** (1 / 3) - (D + Q) ** (1 / 3)
	G = 1 / 2 * ((E ** 2 + v) ** (1 / 2) + E)
	t = (G ** 2 + (F - v * G) / (2 * G - E)) ** (1 / 2) - G

	phi = (np.arctan(a * (1 - t ** 2) / (2 * b * t)))
	h = (R - a * t) * np.cos(phi) + (z - b) * np.sin(phi)
	phi *= z_sign
	lambda_ = np.arctan2(Y, X)

	return np.rad2deg(phi), np.rad2deg(lambda_), h
