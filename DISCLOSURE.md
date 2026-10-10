# Disclosure and attribution

JD Jones is the author and responsible maintainer. OpenAI GPT, Claude (Anthropic), and
Grok (xAI) were used for research, computation, writing, and formalization assistance.
OpenAI GPT prepared the final manuscript and formalization package.

The dimension-five benchmark, including its matrices, exact spectrum, and ratio 19/16,
is due to Christopher De Sa, *Random Reshuffling is Not Always Better* (NeurIPS 2020).
Recht and Ré posed the inequality; Lai and Lim proved its universal form false. The
low-dimensional constructions and supplementary proofs are presented with the source
qualifications in [note/LOW_DIMENSION.md](note/LOW_DIMENSION.md).

The two compared Lean contracts concern fixed-size real and complex counterexamples with
the full Euclidean operator norm. Exact Python arithmetic provides separate checks.
Numerical experiments supply neither proof of nonexistence nor global optimality. The
formal and supplementary scopes are specified in [VERIFICATION.md](VERIFICATION.md).

Automated verification and AI-assisted review are not external human peer review. No
endorsement by the cited authors is claimed.
