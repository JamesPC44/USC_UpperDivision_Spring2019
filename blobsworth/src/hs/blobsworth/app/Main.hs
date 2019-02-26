{-------------------------
 - Author: William Edwards
 - Created On: 2018-10-06
 -
 - All Rights Reserved
-------------------------}

module Main where

import qualified Data.Set as Set
import qualified Data.Vector as Vector
import qualified Data.Map.Strict as Map
import Data.Maybe
import Text.Printf
import Data.List
import Debug.Trace
import qualified System.IO
import qualified GHC.IO.Handle

-- Types

type CellIndex = (Int, Int)
data CellContents = Blank | Obstacle | Goal
  deriving (Show, Eq)
type World = Vector.Vector (Vector.Vector CellContents)
type Node = Set.Set CellIndex
type Problem = (World, Node)
type Entry = (Cost, Node)
type OpenSet = Set.Set Entry
type ClosedSet = Set.Set Node
type Heuristic = Node -> Cost

data Cost = Finite Int | Infinity | NegInfinity | NaN
  deriving (Show, Eq)

instance Ord Cost where
  compare (Finite a) (Finite b) = compare a b
  compare (Finite a) (Infinity) = LT
  compare (Infinity) (Finite b) = GT
  compare (Infinity) (Infinity) = EQ
  compare (NegInfinity) (Finite b) = LT
  compare (Finite a) (NegInfinity) = GT
  compare (NegInfinity) (NegInfinity) = EQ
  compare (NegInfinity) (Infinity) = LT
  compare (Infinity) (NegInfinity) = GT
  compare NaN _ = GT
  compare _ NaN = GT

instance Num Cost where
  (Finite a) + (Finite b) = Finite (a + b)
  (Finite a) + (Infinity) = Infinity
  (Infinity) + (Finite b) = Infinity
  (Infinity) + (Infinity) = Infinity
  (Finite a) + (NegInfinity) = NegInfinity
  (NegInfinity) + (Finite b) = NegInfinity
  (NegInfinity) + (NegInfinity) = NegInfinity
  (NegInfinity) + (Infinity) = NaN
  (Infinity) + (NegInfinity) = NaN
  NaN + _ = NaN
  _ + NaN = NaN
  (Finite a) * (Finite b) = Finite (a * b)
  (Finite a) * (Infinity) = case signum a of 
    1 -> Infinity
    0 -> NaN
    -1 -> NegInfinity
  (Infinity) * (Finite b) = case signum b of 
    1 -> Infinity
    0 -> NaN
    -1 -> NegInfinity
  (Infinity) * (Infinity) = Infinity
  (Finite a) * (NegInfinity) = case signum a of 
    1 -> NegInfinity
    0 -> NaN
    -1 -> Infinity
  (NegInfinity) * (Finite b) = case signum b of 
    1 -> NegInfinity
    0 -> NaN
    -1 -> Infinity
  (NegInfinity) * (NegInfinity) = NegInfinity
  (NegInfinity) * (Infinity) = NegInfinity
  (Infinity) * (NegInfinity) = NegInfinity
  NaN * _ = NaN
  _ * NaN = NaN
  negate (Finite a) = Finite (negate a)
  negate (Infinity) = NegInfinity
  negate (NegInfinity) = Infinity
  negate (NaN) = NaN
  abs (Finite a) = Finite (abs a)
  abs (Infinity) = Infinity
  abs (NegInfinity) = Infinity
  abs (NaN) = NaN
  signum (Finite a) = Finite (signum a)
  signum (Infinity) = Finite 1
  signum (NegInfinity) = Finite 0
  signum (NaN) = Finite 0
  fromInteger n = Finite (fromInteger n)

fromCost :: Cost -> Maybe Int
fromCost (Finite a) = Just a
fromCost Infinity = Nothing
fromCost NegInfinity = Nothing
fromCost NaN = Nothing

data SearchState = SearchState {openSet :: OpenSet,
                                closedSet :: ClosedSet,
                                gVals :: Map.Map Node Cost,
                                fVals :: Map.Map Node Cost,
                                hVals :: Map.Map Node Cost,
                                bps :: Map.Map Node (Maybe Node)
                               } deriving (Show)


-- Constants

translateCost = Finite 1
rearrangeCost = Finite 2

-- Heuristic Code

data RDSearchState = RDSearchState {rdOpenSet :: Set.Set (Cost, CellIndex),
                                    rdGVals :: Map.Map CellIndex Cost
                                   } deriving (Show)

rdExpand :: Problem -> CellIndex -> RDSearchState -> RDSearchState
rdExpand prob currCell state = foldr expandSucc state [(1,0), (-1,0), (0,1), (0,-1)]
  where
    expandSucc (dRow, dCol) state
      | fst succ < 0 || fst succ >= rowBound = state
      | snd succ < 0 || snd succ >= colBound = state
      | ((fst prob) Vector.! (fst succ)) Vector.! (snd succ) == Obstacle = state
      | gCurr + (Finite 1) < gSucc = RDSearchState {rdOpenSet = Set.insert ((gCurr + 1), succ) $ Set.delete (gSucc, succ) $ (rdOpenSet state),
                                                    rdGVals = Map.insert  succ (gCurr + 1 ) (rdGVals state)
                                                   }
      | otherwise = state
      where
        succ = (fst currCell + dRow, snd currCell + dCol)
        gSucc = fromMaybe Infinity $ Map.lookup succ $ rdGVals state
    rowBound = Vector.length $ fst prob
    colBound = Vector.length $ Vector.head $ fst prob
    gCurr = (rdGVals state) Map.! currCell


rDijkstra :: Problem -> RDSearchState -> RDSearchState
rDijkstra prob state
   | Set.null (rdOpenSet state) == True = state
   | otherwise = rDijkstra prob $ rdExpand prob currCell state''
     where
       state'' = RDSearchState {rdOpenSet = Set.delete (currCost, currCell) $ rdOpenSet state',
                                rdGVals = rdGVals state'
                               }
       state' = rdExpand prob currCell state
       (currCost, currCell) = Set.findMin $ rdOpenSet state

computeHeuristic :: Problem -> Heuristic
computeHeuristic prob = (\node -> let val = Set.findMin $ Set.map (\cell -> fromMaybe Infinity $ Map.lookup cell $ rdGVals state) node in val)
  where
    state = rDijkstra prob initState
    initState = RDSearchState {rdOpenSet = Set.singleton (0, goalCell),
                               rdGVals = Map.singleton goalCell (Finite 0)}
    goalCell = head $ filter (\(row, col) -> (fst prob  Vector.! row) Vector.! col == Goal)
                      [(row, col)  | row <- [0..(rowBound-1)], col <- [0..(colBound-1)]] 
    rowBound = Vector.length $ fst prob
    colBound = Vector.length $ Vector.head $ fst prob

showHeuristic :: Problem -> Heuristic -> String
showHeuristic (world, _) heur = unlines $ map getLine [0..(rowBound - 1)]
  where
    getLine row = intercalate "" $ map (maybe "  n  " $ printf "%5d") $ map (\col -> fromCost $ heur $ Set.singleton (row, col)) [0..(colBound-1)]
    rowBound = Vector.length $ world
    colBound = Vector.length $ Vector.head $ world

showNode :: Problem -> Node -> String
showNode (world, _) node = unlines $ map getLine [0..(rowBound - 1)]
  where
    getLine row = intercalate "" $ map (getChar row) [0..(colBound -1)]
    getChar row col
      | Set.member (row, col) node == True = "B"
      | (world Vector.! row) Vector.! col == Obstacle = "*"
      | (world Vector.! row) Vector.! col == Goal = "G"
      | otherwise = "_"
    rowBound = Vector.length $ world
    colBound = Vector.length $ Vector.head $ world


-- Code

loadCellContents :: Char -> CellContents
loadCellContents x
  | x == '_' = Blank
  | x == 'B' = Blank
  | x == '*' = Obstacle
  | x == 'G' = Goal
  | otherwise = Blank

loadProblem :: String -> Problem
loadProblem str = (world, startNode)
  where
    world = Vector.fromList $ map (Vector.fromList . map loadCellContents) gridRows
    startNode = Set.fromList $ concat $ map (\(rownum, row) -> map (\(y,_) -> (rownum, y)) $ filter (\(_,x) -> x == 'B') $ zip [0..] row) $ zip [0..] gridRows
    gridRows = drop 2 $ lines str

getAdjacentCells :: Set.Set CellIndex -> Set.Set CellIndex
getAdjacentCells = Set.fromList . concat . map getAdjIndexes . Set.toList
  where
    getAdjIndexes :: CellIndex -> [CellIndex]
    getAdjIndexes (row, col) = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]

getMaximalComponent :: Node -> Set.Set CellIndex -> Set.Set CellIndex
getMaximalComponent node subset = 
  let
    largerComponent = Set.union subset (Set.intersection node (getAdjacentCells subset))
  in case compare (Set.size largerComponent) (Set.size subset) of
    EQ -> largerComponent
    otherwise -> getMaximalComponent node largerComponent 

isConnected :: Node -> Bool
isConnected node = node == getMaximalComponent node (Set.singleton(Set.elemAt 0 node))

switchIndices :: CellIndex -> CellIndex -> Set.Set CellIndex -> Set.Set CellIndex
switchIndices x y = Set.insert y . Set.delete x


getRearrangements :: Node -> Set.Set (Set.Set CellIndex)
getRearrangements node = Set.fromList $ filter isConnected [switchIndices x y node |
                                                             x <- Set.toList node,
                                                             y <- Set.toList (getAdjacentCells node),
                                                             not $ Set.member y node]

getTranslations :: Node -> Set.Set (Set.Set CellIndex)
getTranslations node = Set.fromList [translate ro co node | (ro, co) <- [(1,0), (-1,0), (0,1), (0,-1)]]
  where
    translate ro co = Set.map (\(row, col) -> (row + ro, col + co))

isCellValid :: World -> CellIndex -> Bool
isCellValid world (row, col)
  | row < 0 || col < 0 = False
  | row >= Vector.length world = False
  | col >= (Vector.length $ Vector.head world) = False
  | ((world Vector.! row) Vector.! col) == Obstacle = False
  | otherwise = True

isValid :: World -> Node -> Bool
isValid world = Set.foldr (\x y -> y && isCellValid world x) True

getSuccessors :: World -> Node -> Set.Set (Cost, Node)
getSuccessors world node = Set.union rearrangements translations
  where
    rearrangements = Set.map (\node -> (rearrangeCost, node)) $ Set.filter (isValid world) $ getRearrangements node
    translations = Set.map (\node -> (translateCost, node)) $ Set.filter (isValid world) $ getTranslations node

expandSuccessor :: Heuristic -> Node -> (Cost, Node) -> SearchState -> SearchState
expandSuccessor heur currNode (edgeCost, succ) state
  = let gCurr = (gVals state) Map.! currNode
        gSucc = Map.findWithDefault Infinity succ (gVals state)
        hSucc = Map.findWithDefault (heur succ) succ (hVals state)
        fSucc = Map.findWithDefault Infinity succ (fVals state)
        gSucc' = gCurr + edgeCost
        fSucc' = gSucc' + hSucc
        openSet' = Set.insert (fSucc', succ) $ Set.delete (fSucc, succ) $ openSet state
        gVals' = Map.insert succ gSucc' $ gVals state 
        hVals' = Map.insert succ hSucc $ hVals state
        fVals' = Map.insert succ fSucc' $ fVals state
        bps' = Map.insert succ (Just currNode) $ bps state
    in case compare gSucc' gSucc of
        LT -> SearchState {openSet = openSet',
                           closedSet = closedSet state,
                           gVals = gVals',
                           hVals = hVals',
                           fVals = fVals',
                           bps = bps'}
        otherwise -> state

expandNode :: Problem -> Heuristic -> Node -> SearchState -> SearchState
expandNode (world, _) heur node state = 
  SearchState {
    openSet = openSet state',
    closedSet = closed',
    gVals = gVals state',
    hVals = hVals state',
    fVals = fVals state',
    bps = bps state'}
  where
    closed' = Set.insert node $ closedSet state'
    state' = expandSuccessors (Set.toList $ getSuccessors world node) state
    expandSuccessors :: [(Cost, Node)] -> SearchState -> SearchState
    expandSuccessors [] s = s
    expandSuccessors (succ:succs) state = let state' = expandSuccessor heur node succ state
                                          in expandSuccessors succs state'

isGoal :: World -> Node -> Bool
isGoal world = Set.foldr (\(row, col) y -> y || (world Vector.! row) Vector.! col == Goal) False

reconstructPath :: SearchState -> Node -> [Node] 
reconstructPath state endNode = reconstruct (bps state) endNode []
  where
    reconstruct :: Map.Map Node (Maybe Node) -> Node -> [Node] -> [Node]
    reconstruct bps node nodes
      | parent == Nothing = nodes
      | otherwise = reconstruct bps (fromJust parent) ((fromJust parent):nodes)
      where
        parent = bps Map.! node

aStarLoop :: Heuristic -> Problem -> SearchState -> Maybe (Cost, [Node])
aStarLoop heur prob state
  | currEntry == Nothing = Nothing
  | isGoal (fst prob) currNode == True = Just $ (gVals state Map.! currNode, reconstructPath state currNode)
  | Set.member currNode (closedSet state) == True = aStarLoop heur prob state'''
  -- | otherwise = traceShow (fst $ fromJust currEntry) $ aStarLoop heur prob state''
  | otherwise = aStarLoop heur prob state'
  where
    currEntry = Set.lookupMin $ openSet state
    currNode = snd $ fromJust currEntry
    state''' =  SearchState {openSet = Set.deleteMin $ openSet state,
                           closedSet = closedSet state,
                           gVals = gVals state,
                           hVals = hVals state,
                           fVals = fVals state,
                           bps = bps state}
    state' = expandNode prob heur currNode state {openSet = Set.deleteMin (openSet state)}

aStarSearch :: Heuristic -> Problem -> Maybe (Cost, [Node])
aStarSearch heur (world, startNode) = aStarLoop heur (world, startNode) initState
  where 
    initState = SearchState {openSet = Set.singleton (initHeur, startNode),
                             closedSet = Set.empty,
                             gVals = Map.singleton startNode (Finite 0),
                             hVals = Map.singleton startNode initHeur,
                             fVals = Map.singleton startNode initHeur,
                             bps = Map.singleton startNode Nothing}
    initHeur = heur startNode

solve :: Problem -> Maybe Int
solve prob = trace (maybe "" (\result -> intercalate "\n\n" $ map (showNode prob) $ snd result) result) $ fromCost $ maybe NaN fst result
  where
    result = aStarSearch heur prob
    heur = computeHeuristic prob

main :: IO ()
main = interact $ (\x -> x++"\n") . show . fromMaybe (-1) . solve . loadProblem

-- program :: String -> String
-- program = (\x -> x++"\n") . show . fromMaybe (-1) . solve . loadProblem
-- 
-- 
-- filename = "../../../../in/004.txt"
-- 
-- main = do
--   input <- readFile filename
--   let output = program input
--   print output

-- main = interact $ (\str -> let prob = loadProblem str in showHeuristic prob $ computeHeuristic prob)

{-
solve :: Problem -> Int


main :: IO ()
-}
