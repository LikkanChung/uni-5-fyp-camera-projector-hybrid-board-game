import os

POSITIVE_DATASETS = {
    'positive_blue',
    'positive_green',
    'positive_purple',
    'positive_red'
}

POSITIVE_COMBINED = 'positive_combined'
PATH = os.path.join('data', POSITIVE_COMBINED)


def combine_descriptor_files():
    lines = []
    for positive_set in POSITIVE_DATASETS:
        with open(os.path.join('data', positive_set, f'{positive_set}.dat'), 'r') as descriptor_file:
            for line in descriptor_file.readlines():
                lines.append(f'{positive_set}/{line}')

    with open(os.path.join('data', f'{POSITIVE_COMBINED}.dat'), 'w') as combined_descriptor_file:
        combined_descriptor_file.writelines(lines)

    print(f'Created a total of {len(lines)} positive samples.')
