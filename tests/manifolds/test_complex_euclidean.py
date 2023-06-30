import numpy as np
import pytest
from numpy import linalg as la
from numpy import random as rnd
from numpy import testing as np_testing

from pymanopt.manifolds import ComplexEuclidean


class TestComplexEuclideanManifold:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.m = m = 10
        self.n = n = 5
        self.man = ComplexEuclidean(m, n)

    def test_dim(self):
        assert self.man.dim == 2 * self.m * self.n

    def test_typicaldist(self):
        np_testing.assert_almost_equal(
            self.man.typicaldist, np.sqrt(self.m * self.n)
        )

    def test_dist(self):
        e = self.man
        x, y = rnd.randn(2, self.m, self.n)
        np_testing.assert_almost_equal(e.dist(x, y), la.norm(x - y))

    def test_inner_product(self):
        e = self.man
        x = e.random_point()
        y = e.random_tangent_vector(x)
        z = e.random_tangent_vector(x)
        np_testing.assert_almost_equal(
            np.real(np.sum(y.conj() * z)), e.inner_product(x, y, z)
        )

    def test_projection(self):
        e = self.man
        x = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.projection(x, u), u)

    def test_euclidean_to_riemannian_hessian(self):
        e = self.man
        x = e.random_point()
        u = e.random_tangent_vector(x)
        egrad, ehess = rnd.randn(2, self.m, self.n)
        np_testing.assert_allclose(
            e.euclidean_to_riemannian_hessian(x, egrad, ehess, u), ehess
        )

    def test_retr(self):
        e = self.man
        x = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.retr(x, u), x + u)

    def test_norm(self):
        e = self.man
        x = e.random_point()
        u = rnd.randn(self.m, self.n)
        np_testing.assert_almost_equal(np.sqrt(np.sum(u**2)), e.norm(x, u))

    def test_random_point(self):
        e = self.man
        x = e.random_point()
        y = e.random_point()
        assert np.shape(x) == (self.m, self.n)
        assert la.norm(x - y) > 1e-6

    def test_random_tangent_vector(self):
        e = self.man
        x = e.random_point()
        u = e.random_tangent_vector(x)
        v = e.random_tangent_vector(x)
        assert np.shape(u) == (self.m, self.n)
        np_testing.assert_almost_equal(la.norm(u), 1)
        assert la.norm(u - v) > 1e-6

    def test_transp(self):
        e = self.man
        x = e.random_point()
        y = e.random_point()
        u = e.random_tangent_vector(x)
        np_testing.assert_allclose(e.transp(x, y, u), u)

    def test_exp_log_inverse(self):
        s = self.man
        X = s.random_point()
        Y = s.random_point()
        Yexplog = s.exp(X, s.log(X, Y))
        np_testing.assert_array_almost_equal(Y, Yexplog)

    def test_log_exp_inverse(self):
        s = self.man
        X = s.random_point()
        U = s.random_tangent_vector(X)
        Ulogexp = s.log(X, s.exp(X, U))
        np_testing.assert_array_almost_equal(U, Ulogexp)

    def test_pairmean(self):
        s = self.man
        X = s.random_point()
        Y = s.random_point()
        Z = s.pairmean(X, Y)
        np_testing.assert_array_almost_equal(s.dist(X, Z), s.dist(Y, Z))
