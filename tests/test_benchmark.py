#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.

import os.path

from miplearn.benchmark import BenchmarkRunner
from miplearn.problems.stab import MaxWeightStableSetGenerator
from scipy.stats import randint

from miplearn.solvers.learning import LearningSolver


def test_benchmark():
    # Generate training and test instances
    generator = MaxWeightStableSetGenerator(n=randint(low=25, high=26))
    train_instances = generator.generate(5)
    test_instances = generator.generate(3)

    # Training phase...
    training_solver = LearningSolver()
    training_solver.parallel_solve(train_instances, n_jobs=10)

    # Test phase...
    test_solvers = {
        "Strategy A": LearningSolver(),
        "Strategy B": LearningSolver(),
    }
    benchmark = BenchmarkRunner(test_solvers)
    benchmark.fit(train_instances)
    benchmark.parallel_solve(test_instances, n_jobs=2, n_trials=2)
    assert benchmark.results.values.shape == (12, 17)

    benchmark.write_csv("/tmp/benchmark.csv")
    assert os.path.isfile("/tmp/benchmark.csv")
