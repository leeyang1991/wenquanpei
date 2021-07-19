#coding=utf-8
'''
download from github
https://gist.github.com/rustyrothwurt/3d207b3af6d1fe04d1e3
date:160621
'''
import datetime
import shutil
import traceback
import os
import sys
import optparse
import csv
# import urllib2
import xml.dom.minidom as dom
import re
import shapefile
import math
import zipfile

DEBUG="off"


def create_bufferxys(inputshp):
	""" METHOD 1 old function for creating a rough 50 meter buffer """
	# example of lat(y) and long (x) for Illinois is 45.12345, -87.12345
	# do everything as xy
	counter = 0
	sf = shapefile.Reader(inputshp)
	poly = get_poly(inputshp)
	allshps = sf.shapeRecords()
	newshapelist = []
	# load the input shapefile
	lenallpts = len(allshps[0].shape.points)
	oldshplist = allshps[0].shape.points
	lastone = lenallpts-1
	counter = 0
	for (thisx,thisy) in allshps[0].shape.points:
		# print "counter is "+str(counter)
		(nextx,nexty) = return_next(oldshplist, counter)
		(prevx,prevy) = return_prev(oldshplist, counter)
		firstangle = calculate_xyangle(prevx, prevy, thisx, thisy)
		secondangle = calculate_xyangle(thisx, thisy, nextx, nexty)
		angleavg = calculate_avgangle(secondangle, firstangle)
		(perpangleone, perpangletwo) = calculate_perpangle(angleavg)
		(newptyl, newptxl) = pointRadialDistance(thisx, thisy, perpangleone)
		(newptyr, newptxr) = pointRadialDistance(thisx, thisy, perpangletwo)
		# now check if within the original poly
		if check_xys_in_poly(newptxl, newptyl, poly):
			print("point is in poly so not adding it")
		else:
			newshapelist.append(((float(newptxl), float(newptyl))))
		if check_xys_in_poly(newptxr, newptyr, poly):
			print("point is in poly so not adding it")
		else:
			newshapelist.append(((float(newptxr), float(newptyr))))
		counter += 1
	# print "adding one more point to finish the polygon"
	do_debug("original shapefile in...")
	do_debug("outgoing shapefile list of new shapes")
	do_debug(str(len(newshapelist)))
	return newshapelist
	#then filter out the ones that are in the polygon


def check_bufferxys(inputshp, x, y):
	#sample y and x are 41.8910658062,-87.636381512
	""" METHOD 2 new function for just checking to see if input points are within the buffered area of 50 meters """
	# example of lat(y) and long (x) for Illinois is 45.12345, -87.12345
	# do everything as xy
	distance = 0.0500000
	sf = shapefile.Reader(inputshp)
	poly = get_poly(inputshp)
	allshps = sf.shapeRecords()
	newshapelist = []
	# load the input shapefile
	lenallpts = len(allshps[0].shape.points)
	oldshplist = allshps[0].shape.points
	counter = 0
	pericheck = "OUT"
	for (thisx,thisy) in oldshplist:
		# print "counter is "+str(counter)
		(prevx,prevy) = return_prev(oldshplist, counter)
		secondtriangle = solve_triangle(x, y, prevx, prevy, thisx, thisy)
		if secondtriangle <= distance:
			pericheck = "IN"
			# print pericheck
			return pericheck
	# print pericheck
	return pericheck


def do_debug(texttoprint):
	if DEBUG == "on":
		print(texttoprint)


def get_poly(shpfile):
	"""assumes shapefile consists of one poly and returns those points"""
	sf = shapefile.Reader(shpfile)
	allshps = sf.shapeRecords()
	### ### ### ### ### ### ### ### ### ###
	### make inputs
	poly = [(float(i[0]),float(i[1])) for i in allshps[0].shape.points]
	return poly



def check_xys_in_poly(xpt, ypt, poly):
	""" pass in a xy and will return true or false if the point is found within the 1 poly"""
	found = ''
	do_debug("starting the check to see if the point is within the polygon")
	if (xpt,ypt) in poly:
		# check if in list of points
		do_debug("found the point in the list of points. Writing to output file")
		found = "INshp"
		return True
	# check if point is on a boundary
	for i in range(len(poly)):
		p1 = None
		p2 = None
		if i==0:
			p1 = poly[0]
			p2 = poly[1]
		else:
			p1 = poly[i-1]
			p2 = poly[i]
		if p1[1] == p2[1] and p1[1] == ypt and xpt > min(p1[0], p2[0]) and xpt < max(p1[0], p2[0]):
			do_debug("found the point on the boundary. Writing to output file")
			found = "INshp"
			return True
			# now check to see if within boundaries
	n = len(poly)
	inside = False
	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if ypt > min(p1y,p2y):
			if ypt <= max(p1y,p2y):
				if xpt <= max(p1x,p2x):
					if p1y != p2y:
						xints = (ypt-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or xpt <= xints:
						inside = not inside
		p1x,p1y = p2x,p2y
	if inside:
		return True
	else:
		return False



def return_prev(inputshplist, order):
	totalIter = len(inputshplist) - 1
	prev = order - 1
	if order == 0:
		# the item is the first in the list
		return inputshplist[totalIter]
	else:
		return inputshplist[prev]

def return_next(inputshplist, order):
	totalIter = len(inputshplist) - 1
	next = order + 1
	if order == totalIter:
		# the item is the last in the list
		return inputshplist[0]
	else:
		return inputshplist[next]


def write_to_shp(inputshplist, outputshp):
	""" Deprecated function for creating a new shapefile from a input of points of xys along a 50 meter buffer """
	w = shapefile.Writer(shapefile.POLYGON)
	w.autoBalance = 1
	w.poly(shapeType=3, parts=[[[float(i[0]),float(i[1])] for i in inputshplist]])
	w.field('FIRST_FLD','C','40')
	w.record('First','Polygon')
	w.save(outputshp)
	return outputshp


def do_debug(texttoprint):
	if DEBUG == "on":
		print(texttoprint)



def pointRadialDistance(x, y, bearing):
	"""Return final coordinates in degrres given initial coordinates and a bearing in degrees for 50 meters"""
	# remember y is y and xg is x and we take in the xy, but we return yx
	distance = 0.0500000
	rEarth = 6371.01000000 # Earth's average radius in km
	epsilon = 0.000000001 # threshold for floating-point equality
	ry1 = math.radians(y)
	rx1 = math.radians(x)
	rbearing = math.radians(bearing)
	rdistance = distance / rEarth # normalize linear distance to radian angle
	ry = ry1 + ( math.sin(rbearing) * rdistance )
	rx = rx1 + ( math.cos(rbearing) * rdistance )
	yout = math.degrees(ry)
	xout = math.degrees(rx)
	return (yout, xout)


def calculate_xyangle(xptone, yptone, xpttwo, ypttwo):
	""" calculates the bearing between two coordinates """
	# calculate the angle between v0, and v1
	# calculate the angle perpendicular to segment(v0-v1)
	# calculate the angle between v1 and v2
	# calculate the angle perpendicular to segment(v1-v2)
	# get the average in degrees between the two angles
	angle = math.degrees(math.atan2(yptone - ypttwo, xptone - xpttwo))
	bearing = ( 90 - angle ) % 360
	bearing1 = (angle + 360) % 360
	return bearing1

def calculate_avgangle(firstangle, secondangle):
	""" returns the average between two numbers """
	anglediff = ( ( float(firstangle) + float(secondangle) ) / 2 )
	return anglediff


def calculate_perpangle(anglediff):
	""" Deprecated calculates two angles perpendicular to one bearing """
	ppangle1 = ''
	ppangle2 = ''
	ppangle1 = ( anglediff - 90 ) % 360
	ppangle2 = ( anglediff + 90 ) % 360
	do_debug("these are the perpindicular angles")
	do_debug(ppangle1)
	do_debug(ppangle2)
	return (ppangle1, ppangle2)





def get_seg_distance(x1, y1, x2, y2):
	""" takes an input x and y and a destination x and y and returns the lengths in km between the points """
	rEarth = 6371.01000000
	x1new = math.radians(x1)
	x2new = math.radians(x2)
	y1new = math.radians(y1)
	y2new = math.radians(y2)
	dlon = x2new - x1new
	dlat = y2new - y1new
	a = math.sin(dlat/2)**2 + math.cos(y1new) * math.cos(y2new) * math.sin(dlon/2)**2
	c = 2 * math.asin(math.sqrt(a))
	km = rEarth * c
	do_debug("length of segment is...")
	do_debug(km)
	return km

def get_triangle_height(sidea, sideb, sidec):
	""" takes the 3 segment sides and returns the height of the triangle """
	do_debug("get_triangle_height")
	# side a is the segment CB (xy0 to pxy)
	do_debug(sidea)
	# side b is the segment AC (xy0 to xy1)
	do_debug(sideb)
	# side c is the segment AB (xy1 to pxy)
	do_debug(sidec)
	angleofA = calc_tri_angle(sideb, sidec, sidea)
	do_debug("Angle A is ")
	do_debug(angleofA)
	# now solve for angles B and C. If Angle B is less than 45 degrees we cannot make 2 perp angles, so we need to just check the vertices which should have already been done.
	angleofB = calc_tri_angle(sidec, sidea, sideb)
	do_debug("Angle B is ")
	do_debug(angleofB)
	angleofC = calc_tri_angle(sidea, sideb, sidec)
	do_debug("Angle C is ")
	do_debug(angleofC)
	if angleofB == "No solution":
		return 99999999
	elif angleofB < 45:
		do_debug("Angle of B is less than 45")
		return 99999999
	else:
		height = get_btri_height(sidea, sideb, sidec)
		do_debug("distance from point to segment is...")
		do_debug(height)
		return height


def calc_tri_angle(sega, segb, segc):
	try:
		temp = ((float(sega) * float(sega)) + (float(segb) * float(segb)) - (float(segc) * float(segc)) ) / (2 * float(sega) * float(segb))
		if ( 1 >= temp >= -1 ):
			return math.degrees(math.acos(temp))
		else:
			return "No solution"
	except:
		return "No solution"
		pass


def get_btri_height(sa, sb, sc):
	ac = math.acos(((float(sb) * float(sb)) + (float(sa) * float(sa)) - (float(sc) * float(sc)) ) / (2 * float(sb) * float(sa)))
	area = float(sa) *  float(sb) * 0.5000000 * math.sin(ac)
	hb = 2 * (area / sb)
	return hb

def solve_triangle(px, py, x1, y1, x2, y2):
	""" takes the 3 points and sends to function for getting the segment lengths and ultimately the distance from the point to the line of the base of the triangle connecting the point and the line segment of the polygon """
	sidea = ''
	sideb = ''
	sidec = ''
	do_debug("Input px py x1 y1 x2 y2 to the solve triangle...")
	do_debug(str(px)+", "+str(py)+", "+str(x1)+", "+str(y1)+", "+str(x2)+", "+str(y2))
	distance = 0.0500000
	# side a is the segment CB (xy0 to pxy)
	sidea = get_seg_distance(x1, y1, px, py)
	#do_debug("Side A from xy0 to pxy is...")
	#do_debug(sidea)
	# side b is the segment AC (xy0 to xy1)
	sideb = get_seg_distance(x1, y1, x2, y2)
	#do_debug("Side B from xy0 to xy1 is...")
	#do_debug(sideb)
	# side c is the segment AB (xy1 to pxy)
	sidec = get_seg_distance(x2, y2, px, py)
	#do_debug("Side C from xy1 to pxy is...")
	#do_debug(sidec)
	height = get_triangle_height(sidea, sideb, sidec)
	if sidea <= distance:
		do_debug("returning side a")
		return sidea
	elif sidec <= distance:
		do_debug("returning side c")
		return sidec
	# now get height if the distances between the xys and pxys are not less than the distance
	else:
		return height