import logging
from enum import Enum
from functools import wraps
from typing import Any, Callable, Generator, List, Optional

from glab.alphabet import String
from glab.ast import Tree
from glab.representation import Representable

log = logging.getLogger("glab.GrammarBase")


class Strategy(Enum):
    """Derivation strategy

    DFS: Depth-First search
    IDS: Iterative deepening DFS
    BFS: Breadth-First search
    """

    DFS = "DFS"
    IDS = "IDS"
    BFS = "BFS"


class ConfigurationBase(Representable):
    def __init__(
        self,
        data: Any,
        parent: "ConfigurationBase" = None,
        used_production: Any = None,
        affected: Any = None,
        depth: int = 0
    ):
        """Inits configuration.

        Args:
            data: Arbitrary data that defines configuration. (e.i. for phrase grammar - sential form)
            parent: Configuration from which was this configuration derived. Only axiom doesn't have parent.
            used_production: Production that was used to obtain this configuration.
            affected: If production does not unambiguously specify derivation step, affected can be used.
            depth: Distance from axiom.
        """
        self.data = data
        self.parent = parent
        self.used_production = used_production
        self.affected = affected
        self.depth = depth

    def __eq__(self, other):
        return isinstance(other, ConfigurationBase) and self.data == other.data

    @property
    def sential_form(self) -> String:
        """Sential form that this configuration represents.

        Language generated by grammar contains all senttial forms that are setences

        Returns:
            String
        """
        return self.data

    def derivation_sequence(self) -> List["ConfigurationBase"]:
        """Return sequence of configuration.

        Sequence starts with axiom and results in self.

        """
        if not self.parent:
            return [self]
        return self.parent.derivation_sequence() + [self]

    def ast_root(self) -> Tree:
        raise NotImplementedError

    def ast_update(self, tree: Tree) -> Tree:
        raise NotImplementedError

    def abstract_syntax_tree(self) -> Tree:
        if not self.parent:
            return self.ast_root()
        tree = self.parent.abstract_syntax_tree()
        return self.ast_update(tree)

    def copy(self):
        """This is shit"""
        return self.__class__(
            self.data,
            self.parent,
            self.used_production,
            self.affected,
        )


class ProductionBase(Representable):
    """Production of grammar

    This class represent one production of grammar.
    Every production is tried to be matched against current configuration and then applied.

    """

    def apply(self, configuration: ConfigurationBase) -> List[ConfigurationBase]:
        pass


class GrammarBase(Representable):
    """Formal grammar

    This class represents formal grammar. Grammar takes configuration and by using production generates
    new configurations

    Attributes:
        configuration_class (ConfigurationBase): Class representing one configuration
        production_class (ProductionBase): Class representing one production
    """

    configuration_class = ConfigurationBase
    production_class = ProductionBase

    def __init__(self):
        self.filters = []

    def set_filter(self, func: Callable[[ConfigurationBase], bool]):
        log.info("Setting filter: %s.", func.__name__)
        self.filters.append(func)

    @property
    def axiom(self) -> ConfigurationBase:
        """Starting configuration.

        Derivation starts from this configuration

        Returns:
            starting configuration
        """
        raise NotImplementedError

    def direct_derive(self, configuration: ConfigurationBase) -> Generator[ConfigurationBase, None, None]:
        """One derivation step.

        Args:
            configuration: Starting configuration

        Returns:
            generator

        """
        raise NotImplementedError

    def _filter(self, configuration: ConfigurationBase):
        for func in self.filters:
            if not func(configuration):
                return False
        return True

    def dfs_derive(self, depth: int):
        log.info("DFS search. (depth=%s)", depth)
        stack = [self.direct_derive(self.axiom)]
        while stack:
            next_configuration = next(stack[-1], None)
            if next_configuration is None:
                stack.pop()
                continue

            if not self._filter(next_configuration):
                continue

            yield next_configuration

            if next_configuration.sential_form.is_sentence:
                continue

            if len(stack) < depth:
                stack.append(self.direct_derive(next_configuration))

    def bfs_derive(self, depth: int):
        log.info("BFS search. (depth=%s)", depth)
        queue = [self.direct_derive(self.axiom)]
        while queue:
            configuration = queue.pop(0)
            for next_configuration in list(configuration):
                if next_configuration.depth > depth:
                    break
                if not self._filter(next_configuration):
                    continue

                yield next_configuration

                if next_configuration.sential_form.is_sentence:
                    continue
                queue.append(self.direct_derive(next_configuration))

    def ids_derive(self, depth: int = None):
        current_depth = 0
        while depth is None or current_depth < depth:
            for configuration in self.dfs_derive(current_depth):
                if configuration.depth == current_depth:
                    yield configuration
            current_depth += 1

    def derive(
        self,
        depth: Optional[int] = None,
        exact_depth: bool = False,
        only_sentences: bool = True,
        strategy: Strategy = Strategy.DFS,
    ) -> Generator[ConfigurationBase, None, None]:
        """Derive from axiom

        Args:
            depth: Maximal depth of derivation. If depth=None, derivation continues indefinitely and IDS is used.
            exact_depth: Yield only configurations with exact depth.
            only_sentences: Yield only sentences.
            strategy: One of DFS, BFS, IDS.

        Returns:

        """
        log.info(
            "Derivation started. (depth=%s, strategy=%s, exact_depth=%s, only_sentences=%s)",
            depth, strategy.value, exact_depth, only_sentences
        )
        log.info("Axiom: %s", self.axiom)

        if depth is None:
            strategy = Strategy.IDS
            exact_depth = False

        algorithms = {
            Strategy.DFS: self.dfs_derive,
            Strategy.BFS: self.bfs_derive,
            Strategy.IDS: self.ids_derive,
        }

        for configuration in algorithms[strategy](depth=depth):
            if exact_depth and depth and configuration.depth != depth:
                continue
            if only_sentences and not configuration.sential_form.is_sentence:
                continue
            yield configuration

    def parse(self, configuration: ConfigurationBase, matches: int = 1) -> ConfigurationBase:
        for derived_configuration in self.derive(strategy=Strategy.IDS):
            if derived_configuration.sential_form == configuration.sential_form:
                yield derived_configuration
                matches -= 1
                if not matches:
                    break


grammar_restriction = Callable[[GrammarBase], None]


def restrictions(factory, *conditions: List[grammar_restriction]):
    """Wrapper around grammar factory which ensures that certian conditions are met.

    Args:
        factory: Grammar factory.
        *conditions: List of callables that expect grammar object and raise error if certian condition is not met

    Returns:
        wrapper
    """

    @wraps(factory)
    def wrapper(*args, **kwargs):
        grammar = factory(*args, **kwargs)
        for condition in conditions:
            log.debug("Imposing restriction: %s", condition.__name__)
            condition(grammar)
        return grammar
    return wrapper
