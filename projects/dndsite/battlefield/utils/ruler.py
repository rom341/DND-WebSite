def ruler(start_x_pos, start_y_pos, end_x_pos, end_y_pos):

    delta_x = int(start_x_pos) - int(end_x_pos)
    delta_y = int(start_y_pos) - int(end_y_pos)

    dlina = delta_x + delta_y

    return abs(dlina)