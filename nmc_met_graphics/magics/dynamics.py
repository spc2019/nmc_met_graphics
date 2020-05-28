# _*_ coding: utf-8 _*_

# Copyright (c) 2020 NMC Developers.
# Distributed under the terms of the GPL V3 License.

"""
Plot atmospheric dynamics maps.
"""

import math
import numpy as np
import xarray as xr
import Magics.macro as magics
from nmc_met_graphics.magics import util, map_set


# global variables
out_png_width = 1200


def draw_wind_upper(uwind, vwind, lon, lat, gh=None, skip_vector=None, 
                    map_region=None, head_info=None, date_obj=None, outfile=None):
    """
    Draw 200hPa wind speed and vector field.

    Args:
        uwind (np.array): u wind component, 2D array, [nlat, nlon]
        vwind (np.array): v wind component, 2D array, [nlat, nlon]
        lon (np.array): longitude, 1D array, [nlon]
        lat (np.array): latitude, 1D array, [nlat]
        gh (np.array): geopotential height, 2D array, [nlat, nlon]
        skip_vector (integer): skip grid number for vector plot
        map_region (list or tuple): the map region limit, [lonmin, lonmax, latmin, latmax]
        head_info (string, optional): head information string. Defaults to None.
        date_obj (datetime, optional): datetime object, like 
            date_obj = dt.datetime.strptime('2016071912','%Y%m%d%H'). Defaults to None.
    """

    # check default parameters
    if skip_vector is None:
        skip_vector = max(math.ceil(len(lon)/70), math.ceil(len(lat)/35))

    # put data into fields
    wind_field = util.minput_2d_vector(uwind, vwind, lon, lat, skip=skip_vector)
    wspeed_field = util.minput_2d(np.sqrt(uwind*uwind + vwind*vwind), lon, lat, {'long_name': 'Wind Speed', 'units': 'm/s'})
    if gh is not None:
        gh_feild = util.minput_2d(gh, lon, lat, {'long_name': 'height', 'units': 'gpm'})

    #
    # set up visual parameters
    #

    # Setting the coordinates of the geographical area
    if map_region is None:
        china_map = map_set.get_mmap(
            name='CHINA_CYLINDRICAL',
            subpage_frame_thickness = 5)
    else:
        china_map = map_set.get_mmap(
            name='CHINA_REGION_CYLINDRICAL',
            map_region=map_region,
            subpage_frame_thickness = 5)

    # Background Coaslines
    coastlines = map_set.get_mcoast(name='COAST_FILL')
    china_coastlines = map_set.get_mcoast(name='PROVINCE')

    # Define the simple contouring for gh
    gh_contour = magics.mcont(
        legend= 'off', 
        contour_level_selection_type= 'interval',
        contour_interval= 50.,
        contour_line_colour= 'black',
        contour_line_thickness= 1,
        contour_label= 'on',
        contour_label_height= 0.5,
        contour_highlight_colour= 'black',
        contour_highlight_thickness= 2)

    # Define the shading for the wind speed
    wspeed_contour = magics.mcont(
        legend= 'on',
        contour_level_selection_type= 'level_list', 
        contour_level_list= [30., 40., 50., 60., 70., 80., 90., 100.], 
        contour_shade= 'on', 
        contour_shade_max_level_colour= 'evergreen', 
        contour_shade_min_level_colour= 'yellow',
        contour_shade_method= 'area_fill', 
        contour_reference_level= 0., 
        contour_highlight= 'off', 
        contour_hilo= 'hi', 
        contour_hilo_format= '(F3.0)', 
        contour_hilo_height= 0.6, 
        contour_hilo_type= 'number', 
        contour_hilo_window_size=10,
        contour_label= 'off')

    # Define the wind vector
    wind_vector = magics.mwind(
        legend= 'on',
        wind_field_type= 'arrows',
        wind_arrow_head_shape=1,
        wind_arrow_thickness= 0.5,
        wind_arrow_unit_velocity=50,
        wind_arrow_colour= 'evergreen')

    # Add a legend
    legend = magics.mlegend(
        legend= 'on',
        legend_text_colour= 'black',
        legend_box_mode= 'legend_box_mode',
        legend_automatic_position= 'right',
        legend_border= 'off',
        legend_border_colour= 'black',
        legend_box_blanking= 'on',
        legend_display_type= 'continuous',
        legend_title = "on",
        legend_title_text= "Wind Speed",
        legend_text_font_size = "0.5")

    # Add the title
    text_lines = []
    if head_info is not None:
        text_lines.append("<font size='1'>{}</font>".format(head_info))
    else:
        text_lines.append("<font size='1'>200hPa Wind[m/s] and Height[gpm]</font>")
    if date_obj is not None:
        text_lines.append("<font size='0.8' colour='red'>{}</font>".format(date_obj.strftime("%Y/%m/%d %H:%M(UTC)")))
    title = magics.mtext(
        text_lines = text_lines,
        text_justification = 'left',
        text_font_size = 0.6,
        text_mode = "title",
        text_colour = 'charcoal')

    # draw the figure
    if outfile is not None:
        output = magics.output(
            output_formats= ['png'],
            output_name_first_page_number= 'off',
            output_width= out_png_width,
            output_name= outfile)

        if gh is not None:
            magics.plot(
                output, china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            magics.plot(
                output, china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, legend, title, china_coastlines)
    else:
        if gh is not None:
            return magics.plot(
                china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            return magics.plot(
                china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, legend, title, china_coastlines)


def draw_wind_high(uwind, vwind, lon, lat, gh=None, skip_vector=None, 
                   map_region=None, head_info=None, date_obj=None, outfile=None):
    """
    Draw high wind speed and flags.

    Args:
        uwind (np.array): u wind component, 2D array, [nlat, nlon]
        vwind (np.array): v wind component, 2D array, [nlat, nlon]
        lon (np.array): longitude, 1D array, [nlon]
        lat (np.array): latitude, 1D array, [nlat]
        gh (np.array): geopotential height, 2D array, [nlat, nlon]
        skip_vector (integer): skip grid number for vector plot
        map_region (list or tuple): the map region limit, [lonmin, lonmax, latmin, latmax]
        head_info (string, optional): head information string. Defaults to None.
        date_obj (datetime, optional): datetime object, like 
            date_obj = dt.datetime.strptime('2016071912','%Y%m%d%H'). Defaults to None.
    """

    # check default parameters
    if skip_vector is None:
        skip_vector = max(math.ceil(len(lon)/70), math.ceil(len(lat)/35))

    # put data into fields
    wind_field = util.minput_2d_vector(uwind, vwind, lon, lat, skip=skip_vector)
    wspeed_field = util.minput_2d(np.sqrt(uwind*uwind + vwind*vwind), lon, lat, {'long_name': 'Wind Speed', 'units': 'm/s'})
    if gh is not None:
        gh_feild = util.minput_2d(gh, lon, lat, {'long_name': 'height', 'units': 'gpm'})

    #
    # set up visual parameters
    #

    # Setting the coordinates of the geographical area
    if map_region is None:
        china_map = map_set.get_mmap(
            name='CHINA_CYLINDRICAL',
            subpage_frame_thickness = 5)
    else:
        china_map = map_set.get_mmap(
            name='CHINA_REGION_CYLINDRICAL',
            map_region=map_region,
            subpage_frame_thickness = 5)

    # Background Coaslines
    coastlines = map_set.get_mcoast(name='COAST_FILL')
    china_coastlines = map_set.get_mcoast(name='PROVINCE')

    # Define the simple contouring for gh
    gh_contour = magics.mcont(
        legend= 'off', 
        contour_level_selection_type= 'interval',
        contour_interval= 20.,
        contour_reference_level= 5880.,
        contour_line_colour= 'black',
        contour_line_thickness= 1.5,
        contour_label= 'on',
        contour_label_height= 0.5,
        contour_highlight_colour= 'black',
        contour_highlight_thickness= 3)

    # Define the shading for the wind speed
    wspeed_contour = magics.mcont(
        legend= 'on',
        contour_level_selection_type= 'interval', 
        contour_shade_max_level= 44.,
        contour_shade_min_level= 8., 
        contour_interval= 4.,
        contour_shade= 'on', 
        contour= "off",
        contour_shade_method= 'area_fill', 
        contour_shade_colour_method = 'palette',
        contour_shade_palette_name = 'eccharts_rainbow_blue_purple_9',
        contour_reference_level= 8., 
        contour_highlight= 'off', 
        contour_hilo= 'hi', 
        contour_hilo_format= '(F3.0)', 
        contour_hilo_height= 0.6, 
        contour_hilo_type= 'number', 
        contour_hilo_window_size=10,
        contour_label= 'off')

    # Define the wind vector
    wind_vector = magics.mwind(
        legend= 'off',
        wind_field_type= 'flags',
        wind_flag_length = 0.6,
        wind_thinning_factor= 2.,
        wind_flag_style= 'solid', 
        wind_flag_thickness= 1,
        wind_flag_origin_marker = 'dot',
        wind_flag_min_speed = 0.0,
        wind_flag_colour = 'charcoal')

    # Add a legend
    legend = magics.mlegend(
        legend= 'on',
        legend_text_colour= 'black',
        legend_box_mode= 'legend_box_mode',
        legend_automatic_position= 'right',
        legend_border= 'off',
        legend_border_colour= 'black',
        legend_box_blanking= 'on',
        legend_display_type= 'continuous',
        legend_title = "on",
        legend_title_text= "Wind Speed",
        legend_text_font_size = "0.5")

    # Add the title
    text_lines = []
    if head_info is not None:
        text_lines.append("<font size='1'>{}</font>".format(head_info))
    else:
        text_lines.append("<font size='1'>850hPa Wind[m/s] and 500hPa Height[gpm]</font>")
    if date_obj is not None:
        text_lines.append("<font size='0.8' colour='red'>{}</font>".format(date_obj.strftime("%Y/%m/%d %H:%M(UTC)")))
    title = magics.mtext(
        text_lines = text_lines,
        text_justification = 'left',
        text_font_size = 0.6,
        text_mode = "title",
        text_colour = 'charcoal')

    # draw the figure
    if outfile is not None:
        output = magics.output(
            output_formats= ['png'],
            output_name_first_page_number= 'off',
            output_width= out_png_width,
            output_name= outfile)

        if gh is not None:
            magics.plot(
                output, china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            magics.plot(
                output, china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, legend, title, china_coastlines)
    else:
        if gh is not None:
            return magics.plot(
                china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            return magics.plot(
                china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, legend, title, china_coastlines)


def draw_vort_high(uwind, vwind, vort, lon, lat, gh=None, skip_vector=None, 
                   map_region=None, head_info=None, date_obj=None, outfile=None):
    """
    Draw high wind speed and flags.vort

    Args:
        uwind (np.array): u wind component, 2D array, [nlat, nlon]
        vwind (np.array): v wind component, 2D array, [nlat, nlon]
        vort (np.array):
        lon (np.array): longitude, 1D array, [nlon]
        lat (np.array): latitude, 1D array, [nlat]
        gh (np.array): geopotential height, 2D array, [nlat, nlon]
        skip_vector (integer): skip grid number for vector plot
        map_region (list or tuple): the map region limit, [lonmin, lonmax, latmin, latmax]
        head_info (string, optional): head information string. Defaults to None.
        date_obj (datetime, optional): datetime object, like 
            date_obj = dt.datetime.strptime('2016071912','%Y%m%d%H'). Defaults to None.
    """

    # check default parameters
    if skip_vector is None:
        skip_vector = max(math.ceil(len(lon)/70), math.ceil(len(lat)/35))

    # put data into fields
    wind_field = util.minput_2d_vector(uwind, vwind, lon, lat, skip=skip_vector)
    wspeed_field = util.minput_2d(np.sqrt(uwind*uwind + vwind*vwind), lon, lat, {'long_name': 'Wind Speed', 'units': 'm/s'})
    if gh is not None:
        gh_feild = util.minput_2d(gh, lon, lat, {'long_name': 'height', 'units': 'gpm'})

    #
    # set up visual parameters
    #

    # Setting the coordinates of the geographical area
    if map_region is None:
        china_map = map_set.get_mmap(
            name='CHINA_CYLINDRICAL',
            subpage_frame_thickness = 5)
    else:
        china_map = map_set.get_mmap(
            name='CHINA_REGION_CYLINDRICAL',
            map_region=map_region,
            subpage_frame_thickness = 5)

    # Background Coaslines
    coastlines = map_set.get_mcoast(name='COAST_FILL')
    china_coastlines = map_set.get_mcoast(name='PROVINCE')

    # Define the simple contouring for gh
    gh_contour = magics.mcont(
        legend= 'off', 
        contour_level_selection_type= 'interval',
        contour_interval= 20.,
        contour_reference_level= 5880.,
        contour_line_colour= 'black',
        contour_line_thickness= 1.5,
        contour_label= 'on',
        contour_label_height= 0.5,
        contour_highlight_colour= 'black',
        contour_highlight_thickness= 3)

    # Define the shading for the wind speed
    wspeed_contour = magics.mcont(
        legend= 'on',
        contour_level_selection_type= 'interval', 
        contour_shade_max_level= 44.,
        contour_shade_min_level= 8., 
        contour_interval= 4.,
        contour_shade= 'on', 
        contour= "off",
        contour_shade_method= 'area_fill', 
        contour_shade_colour_method = 'palette',
        contour_shade_palette_name = 'eccharts_rainbow_blue_purple_9',
        contour_reference_level= 8., 
        contour_highlight= 'off', 
        contour_hilo= 'hi', 
        contour_hilo_format= '(F3.0)', 
        contour_hilo_height= 0.6, 
        contour_hilo_type= 'number', 
        contour_hilo_window_size=10,
        contour_label= 'off')

    # Define the wind vector
    wind_vector = magics.mwind(
        legend= 'off',
        wind_field_type= 'flags',
        wind_flag_length = 0.6,
        wind_thinning_factor= 2.,
        wind_flag_style= 'solid', 
        wind_flag_thickness= 1,
        wind_flag_origin_marker = 'dot',
        wind_flag_min_speed = 0.0,
        wind_flag_colour = 'charcoal')

    # Add a legend
    legend = magics.mlegend(
        legend= 'on',
        legend_text_colour= 'black',
        legend_box_mode= 'legend_box_mode',
        legend_automatic_position= 'right',
        legend_border= 'off',
        legend_border_colour= 'black',
        legend_box_blanking= 'on',
        legend_display_type= 'continuous',
        legend_title = "on",
        legend_title_text= "Wind Speed",
        legend_text_font_size = "0.5")

    # Add the title
    text_lines = []
    if head_info is not None:
        text_lines.append("<font size='1'>{}</font>".format(head_info))
    else:
        text_lines.append("<font size='1'>850hPa Wind[m/s] and 500hPa Height[gpm]</font>")
    if date_obj is not None:
        text_lines.append("<font size='0.8' colour='red'>{}</font>".format(date_obj.strftime("%Y/%m/%d %H:%M(UTC)")))
    title = magics.mtext(
        text_lines = text_lines,
        text_justification = 'left',
        text_font_size = 0.6,
        text_mode = "title",
        text_colour = 'charcoal')

    # draw the figure
    if outfile is not None:
        output = magics.output(
            output_formats= ['png'],
            output_name_first_page_number= 'off',
            output_width= out_png_width,
            output_name= outfile)

        if gh is not None:
            magics.plot(
                output, china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            magics.plot(
                output, china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, legend, title, china_coastlines)
    else:
        if gh is not None:
            return magics.plot(
                china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            return magics.plot(
                china_map, coastlines, wspeed_field, wspeed_contour,
                wind_field, wind_vector, legend, title, china_coastlines)


def draw_mslp(mslp, lon, lat, gh=None, map_region=None, 
              head_info=None, date_obj=None, outfile=None):
    """
    Draw mean sea level pressure field.

    Args:
        mslp (np.array): sea level pressure field (mb), 2D array, [nlat, nlon]
        lon (np.array): longitude, 1D array, [nlon]
        lat (np.array): latitude, 1D array, [nlat]
        gh (np.array): geopotential height, 2D array, [nlat, nlon]
        map_region (list or tuple): the map region limit, [lonmin, lonmax, latmin, latmax]
        head_info (string, optional): head information string. Defaults to None.
        date_obj (datetime, optional): datetime object, like 
            date_obj = dt.datetime.strptime('2016071912','%Y%m%d%H'). Defaults to None.
    """

    # put data into fields
    mslp_field = util.minput_2d(mslp, lon, lat, {'long_name': 'Sea level pressure', 'units': 'mb'})
    if gh is not None:
        gh_feild = util.minput_2d(gh, lon, lat, {'long_name': 'height', 'units': 'gpm'})

    #
    # set up visual parameters
    #

    # Setting the coordinates of the geographical area
    if map_region is None:
        china_map = map_set.get_mmap(
            name='CHINA_CYLINDRICAL',
            subpage_frame_thickness = 5)
    else:
        china_map = map_set.get_mmap(
            name='CHINA_REGION_CYLINDRICAL',
            map_region=map_region,
            subpage_frame_thickness = 5)

    # Background Coaslines
    coastlines = map_set.get_mcoast(name='COAST_FILL')
    china_coastlines = map_set.get_mcoast(name='PROVINCE')

    # Define the simple contouring for gh
    gh_contour = magics.mcont(
        legend= 'off', 
        contour_level_selection_type= 'interval',
        contour_interval= 20.,
        contour_reference_level= 5880.,
        contour_line_colour= 'black',
        contour_line_thickness= 1.5,
        contour_label= 'on',
        contour_label_height= 0.5,
        contour_highlight_colour= 'black',
        contour_highlight_thickness= 3)

    # Define the shading for teperature
    mslp_contour = magics.mcont(
        legend= 'on',
        contour_shade= "on",
        contour_hilo= "on",
        contour_hilo_height= 0.6,
        contour_hi_colour= 'blue',
        contour_lo_colour= 'red',
        contour_hilo_window_size= 5,
        contour= "off",
        contour_label= "off",
        contour_shade_method= "area_fill",
        contour_level_selection_type= "level_list",
        contour_level_list=  [940.+i*2.5 for i in range(51)],
        contour_shade_colour_method= "list",
        contour_shade_colour_list= [
            '#FD90EB', '#EB78E5', '#EF53E0', '#F11FD3', '#F11FD3', '#A20E9B', '#880576', '#6D0258', '#5F0853', 
            '#2A0DA8', '#2F1AA7', '#3D27B4', '#3F3CB6', '#6D5CDE', '#A28CF9', '#C1B3FF', '#DDDCFE', '#1861DB',
            '#206CE5', '#2484F4', '#52A5EE', '#91D4FF', '#B2EFF8', '#DEFEFF', '#C9FDBD', '#91F78B', '#53ED54',
            '#1DB31E', '#0CA104', '#FFF9A4', '#FFE27F', '#FAC235', '#FF9D04', '#FF5E00', '#F83302', '#E01304',
            '#A20200', '#603329', '#8C6653', '#B18981', '#DDC0B3', '#F8A3A2', '#DD6663', '#CA3C3B', '#A1241D', 
            '#6C6F6D', '#8A8A8A', '#AAAAAA', '#C5C5C5', '#D5D5D5', '#E7E3E4'])

    # Add a legend
    legend = magics.mlegend(
        legend= 'on',
        legend_text_colour= 'black',
        legend_box_mode= 'legend_box_mode',
        legend_automatic_position= 'right',
        legend_border= 'off',
        legend_border_colour= 'black',
        legend_box_blanking= 'on',
        legend_display_type= 'continuous',
        legend_title = "on",
        legend_title_text= "Pressure",
        legend_label_frequency= 2,
        legend_text_font_size = "0.5")

    # Add the title
    text_lines = []
    if head_info is not None:
        text_lines.append("<font size='1'>{}</font>".format(head_info))
    else:
        text_lines.append("<font size='1'>Mean sea level pressure[mb] and 500hPa Height[gpm]</font>")
    if date_obj is not None:
        text_lines.append("<font size='0.8' colour='red'>{}</font>".format(date_obj.strftime("%Y/%m/%d %H:%M(UTC)")))
    title = magics.mtext(
        text_lines = text_lines,
        text_justification = 'left',
        text_font_size = 0.6,
        text_mode = "title",
        text_colour = 'charcoal')

    # draw the figure
    if outfile is not None:
        output = magics.output(
            output_formats= ['png'],
            output_name_first_page_number= 'off',
            output_width= out_png_width,
            output_name= outfile)

        if gh is not None:
            magics.plot(
                output, china_map, coastlines, mslp_field, mslp_contour,
                gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            magics.plot(
                output, china_map, coastlines,  mslp_field, mslp_contour,
                legend, title, china_coastlines)
    else:
        if gh is not None:
            return magics.plot(
                china_map, coastlines, mslp_field, mslp_contour,
                gh_feild, gh_contour, legend, title, china_coastlines)
        else:
            return magics.plot(
                china_map, coastlines, mslp_field, mslp_contour,
                legend, title, china_coastlines)