// The polling function
function poll(fn, timeout, interval) {
    var endTime = Number(new Date()) + (timeout || 2000);
    interval = interval || 100;

    var checkCondition = async (resolve, reject) => {
        // If the condition is met, we're done! 
        let result = await fn();

        if (result) {
            resolve(result);
        }
        // If the condition isn't met but the timeout hasn't elapsed, go again
        if (Number(new Date()) < endTime) {
            setTimeout(checkCondition, interval, resolve, reject);
        }
        // Didn't match and too much time, reject!
        else {
            reject(new Error('timed out for ' + fn + ': ' + arguments));
        }
    };

    return new Promise(checkCondition);
}

export default poll