//   The polling function
function poll(fn, callback, timeout, interval) {
    var endTime = Number(new Date()) + (timeout || 2000);
    interval = interval || 100;

    (function p() {
        // If the condition is met, we're done!
        if (fn()) {
        callback();
        }
        // If the condition isn't met but the timeout hasn't elapsed, go again
        else if (Number(new Date()) < endTime) {
        setTimeout(p, interval);
        }
        // Didn't match and too much time, reject!
        else {
        callback(new Error('timed out for ' + fn + ': ' + arguments));
        }
    })();
}

export default poll;