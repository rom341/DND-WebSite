def ruler(start_x_pos, start_y_pos, end_x_pos, end_y_pos):

    delta_x = start_x_pos - end_x_pos
    delta_y = start_y_pos - end_y_pos

    dlina = delta_x + delta_y

    return abs(dlina)