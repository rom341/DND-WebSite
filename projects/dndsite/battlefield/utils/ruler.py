def ruler(start_x_pos, start_y_pos, end_x_pos, end_y_pos):

    delta_x = int(start_x_pos) - int(end_x_pos)
    delta_y = int(start_y_pos) - int(end_y_pos)

    modul_x = abs(delta_x)
    modul_y = abs(delta_y)
    dlina = modul_x + modul_y

    return dlina