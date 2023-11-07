import datetime
from subprocess import check_output

log_msg_template_attack_start = '({0}) {1};{2}; Start\n'   # Date, Time; Attack type; parameters
log_msg_template_attack_end = '({0}) {1}; End\n'   # Date, Time; Attack type
log_msg_template_attack_mid = '({0}) {1}\n'   # Time; Command


def log(msg_type, command=None, attack_type=None, param_info=None,
        is_also_printed=False, log_file_name='log.txt'):
    global log_msg_template_attack_start, log_msg_template_attack_end, log_msg_template_attack_mid

    time_now = datetime.datetime.now()
    date_time_str = time_now.strftime('%Y-%m-%d %X')
    time_str = time_now.strftime('%X')

    if msg_type == 'Start' and attack_type is not None:
        param_string = ''
        if type(param_info) is dict:
            for key in param_info:
                param_string += f'{key}={param_info[key]};'
            # if 'intensity' in param_info:
            #     param_string += ('intensity=' + str(param_info['intensity']))
            # else:
            #     param_string += 'intensity=-1'
        msg = log_msg_template_attack_start.format(date_time_str, 'type=' + attack_type, param_string)
    elif msg_type == 'Mid' and command is not None:
        msg = log_msg_template_attack_mid.format(time_str, command)
    elif msg_type == 'End' and attack_type is not None:
        msg = log_msg_template_attack_end.format(date_time_str, 'type=' + attack_type)
    else:
        raise NotImplementedError

    if is_also_printed is True:
        print(msg)
    _write_in_logfile(msg, log_file_name)


def _write_in_logfile(msg_to_be_written, file_name):
    with open(file_name, 'at') as log_file:
        log_file.write(msg_to_be_written)


