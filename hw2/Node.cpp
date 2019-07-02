#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cstring>
#include <ctime>
#include <iostream>
#include <algorithm>

#include "Node.h"
#include "Judge.h"

using namespace std;

Node::Node(int **_board, int *_top, int _M, int _N, int _noX, int _noY, int _turn, Node *_fa, int lastX, int lastY)
	:board(_board), top(_top), M(_M), N(_N), noX(_noX), noY(_noY), turn(_turn), fa(_fa), lastMoveX(lastX), lastMoveY(lastY), totScore(0), searchTime(1) {
	child = new Node*[_N];
	childNum = totChildNum = 0;
	for (int i = 0; i < _N; i++) {
		if (_top[i] > 0) totChildNum++;
		child[i] = nullptr;
	}
}
bool Node::ableToExpand() {
	return childNum < totChildNum;
}
Node* Node::expand() {
	while (1) {
		int pos = rand() % N;
		if (top[pos] && (child[pos] == nullptr)) {
			childNum++;
			int **nextBoard = new int*[M];
			int *nextTop = new int[N];
			for (int i = 0; i < N; i++) nextTop[i] = top[i];
			for (int i = 0; i < M; i++) {
				nextBoard[i] = new int[N];
				for (int j = 0; j < N; j++) nextBoard[i][j] = board[i][j];
			}
			nextTop[pos]--;
			nextBoard[nextTop[pos]][pos] = turn;
			if ((pos == noY) && (nextTop[pos] - 1 == noX)) nextTop[pos]--;
			child[pos] = new Node(nextBoard, nextTop, M, N, noX, noY, 3 - turn, this, top[pos] - 1, pos);
			return child[pos];
		}
	}
}
Node* Node::bestChild(double c) {
	double maxScore = -1e100;
	Node *best = nullptr;
	for (int i = 0; i < N; i++) if (child[i] != nullptr) {
		double chScore = (double)(-child[i]->totScore) / child[i]->searchTime + c * sqrt(2 * log(searchTime) / child[i]->searchTime);
		if (chScore > maxScore) {
			maxScore = chScore;
			best = child[i];
		}
	}
	return best;
}
void Node::backprop(int delta) {
	Node *p = this;
	while (p != nullptr) {
		p->searchTime++;
		p->totScore += delta;
		delta = -delta;
		p = p->fa;
	}
}
bool Node::gameEnd() {
	if (lastMoveX == -1 || lastMoveY == -1) return false;
	if (turn == 2) {
		if (userWin(lastMoveX, lastMoveY, M, N, board)) return true;
		if (isTie(N, top)) return true;
	} else {
		if (machineWin(lastMoveX, lastMoveY, M, N, board)) return true;
		if (isTie(N, top)) return true;
	}
	return false;
}
int Node::score() {
	if (turn == 2) {
		if (userWin(lastMoveX, lastMoveY, M, N, board)) return -1;
		if (isTie(N, top)) return 0;
	} else {
		if (machineWin(lastMoveX, lastMoveY, M, N, board)) return -1;
		if (isTie(N, top)) return 0;
	}
}
int Node::MonteCarlo() {
	int **_board = new int*[M];
	int *_top = new int[N];
	for (int i = 0; i < M; i++) {
		_board[i] = new int[N];
		for (int j = 0; j < N; j++) _board[i][j] = board[i][j];
	}
	for (int i = 0; i < N; i++) _top[i] = top[i];
	int player = turn;
	int result = 0;
	while (1) {
		int pos = rand() % N;
		while (_top[pos] == 0) pos = rand() % N;
		int x = _top[pos] - 1, y = pos;
		_board[x][y] = player;
		if ((x - 1 == noX) && (y == noY)) _top[pos] = x - 1; else _top[pos] = x;
		if (player == 2) {
			if (machineWin(x, y, M, N, _board)) {
				result = 1; break;
			} else if (isTie(N, _top)) {
				result = 0; break;
			}
		} else {
			if (userWin(x, y, M, N, _board)) {
				result = 1; break;
			} else if (isTie(N, _top)) {
				result = 0; break;
			}
		}
		player = 3 - player;
	}
	delete [] _top;
	for (int i = 0; i < M; i++) delete [] _board[i];
	delete [] _board;
	if (player == turn) return result; else return -result;
}
void Node::print() {
	for (int i = 0; i < N; i++)
		if (child[i] != nullptr) printf("%.4lf ", (double)(-child[i]->totScore) / child[i]->searchTime);
	puts("");
}
Node::~Node() {
	for (int i = 0; i < M; i++) delete [] board[i];
	delete [] board;
	delete [] top;
	for (int i = 0; i < N; i++) if (child[i] != nullptr) delete child[i];
	delete [] child;
}
