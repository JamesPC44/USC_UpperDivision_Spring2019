{-------------------------
 - Author: William Edwards
 - Created On: 2018-10-06
 - 
 - All Rights Reserved
-------------------------}

module Main where

import qualified Data.Set as Set
import qualified Data.Vector as Vector

-- Types

type CellIndex = (Int, Int)
data CellContents = Blank | Obstacle | Goal
  deriving (Show)
type World = Vector.Vector (Vector.Vector CellContents)
type Node = Set.Set CellIndex
type Problem = (World, Node)
type Entry = (Int, Node)
type OpenSet = Set.Set Entry
type ClosedSet = Set.Set Node
type Heuristic = Node -> Int

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

main :: IO ()
main = interact $ show . loadProblem

{-
isValid :: World -> Node -> Node


getSuccessors :: World -> Node -> [Node]


solve :: Problem -> Int


main :: IO ()
main = interact $ show . solve . loadProblem
-}
