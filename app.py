from flask import Flask, request, jsonify
import random
import re
import sys

app = Flask(__name__)

SPEC = re.compile('^(\d+)d(\d+) ?(\w+)?$')
HIDDEN = ('hide', 'hidden', 'invisible', 'ephemeral', 'private')


USAGE = 'USAGE:\n' \
    '`/roll [n]d[x] [options]`\n' \
    'where:\n' \
    '   n == number of dice\n' \
    '   x == number of sides on each die\n' \
    'e.g. `/roll 3d6` will roll 3 6-sided dice. ' \
    '[options] may be any of (hide|hidden|invisible|ephemeral|private) ' \
    'for a private roll.'


def do_roll(spec):
    match = SPEC.match(spec)
    if match is None:
        return {
            'response_type': 'ephemeral',
            'text': 'ERROR: invalid roll command `%s`\n\n%s' % (
                spec, USAGE)
        }
    num = int(match.group(1))
    size = int(match.group(2))
    flag = match.group(3)
    if flag is not None and flag not in HIDDEN:
        return {
            'response_type': 'ephemeral',
            'text': 'ERROR: unrecognized modifier `%s`' % flag
        }
    vals = []
    for i in range(0, num):
        vals.append(random.randint(1, size))
    data = {
        'response_type': 'ephemeral' if flag in HIDDEN else 'in_channel'
    }
    if num == 1:
        data['text'] = str(vals[0])
    else:
        data['text'] = '%s = %d' %  (
            ' + '.join([str(v) for v in vals]), sum(vals))
    return data


@app.route("/", methods=['GET', 'POST'])
def roll():
    try:
        if request.method == 'POST':
            spec = request.form['text']
        else:
            spec = request.args['spec']
        return jsonify(do_roll(spec))
    except:
        return jsonify({
            'response_type': 'ephemeral',
            'text': USAGE
        })


if __name__ == "__main__":
    app.run(debug=True)



