const Proportional = ({
    step = 60 * 60 * 2
} = {}) => {
    const state = {
        lastRunFor: 0,
        totalRuns: 0,
        runAfter: 0
    };

    return ({currentRun = 0, z}) => {
        state.z = z;
        if (!state.totalRuns) {
            state.totalRuns = state.totalRuns + 1;
            state.lastRunFor = currentRun;
            state.runAfter = step;
            return state;
        } else if (currentRun < state.lastRunFor) {
            state.totalRuns = state.totalRuns + 1;
            state.runAfter = Math.ceil(state.runAfter * (state.lastRunFor / currentRun));
            state.lastRunFor = currentRun;
            return state;
        } else if (currentRun === state.lastRunFor) {
            state.totalRuns = state.totalRuns + 1;
            return state;
        } else if (currentRun > state.lastRunFor) {
            const p = 1 - (Math.ceil((state.lastRunFor / currentRun) * 100) / 100);
            state.runAfter = Math.ceil((state.runAfter - (state.runAfter * p)));
            state.lastRunFor = currentRun;
            return state;
        }
    };
};

const Static = ({
    step = 60 * 60 * 3
} = {}) => {
    const state = {
        lastRunFor: 0,
        totalRuns: 0,
        runAfter: 0
    };

    return ({currentRun = 0, z}) => {
        state.z = z;
        state.totalRuns = state.totalRuns + 1;
        state.lastRunFor = currentRun;
        state.runAfter = step;
        return state;
    };
};

module.exports = {
    Proportional,
    Static
};
