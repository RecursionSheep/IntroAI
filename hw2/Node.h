#pragma once

class Node {
	int **board, *top;
	int M, N, noX, noY;
	Node *fa, **child;
	int turn;
	int childNum, totChildNum;
public:
	int lastMoveX, lastMoveY;
	int totScore, searchTime;
	Node(int **_board, int *_top, int _M, int _N, int _noX, int _noY, int _turn, Node *_fa, int lastX, int lastY);
	bool ableToExpand();
	Node* expand();
	Node* bestChild(double c);
	void backprop(int delta);
	bool gameEnd();
	int score();
	void print();
	int MonteCarlo();
	~Node();
};
