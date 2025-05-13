// string_algorithms.h

#ifndef STRING_ALGORITHMS_H
#define STRING_ALGORITHMS_H

#include <stdbool.h>

// --- TRIE (lowercase 'a'–'z') ---
typedef struct TrieNode {
    int count;                  // # of words in this subtree
    int end;                    // # of words ending here
    struct TrieNode *next[26];
} TrieNode;

TrieNode* trie_create_node(void);
void trie_insert(TrieNode *root, const char *s);
bool trie_search(TrieNode *root, const char *s);
int  trie_count_prefix(TrieNode *root, const char *p);
int  trie_longest_prefix_match(TrieNode *root, const char *s);
int  trie_first_mismatch_index(TrieNode *root, const char *s);
void trie_free(TrieNode *root);

// --- RABIN–KARP (polynomial rolling hash) ---
bool is_substring_rk(const char *pattern, const char *text);
int  count_rk_unoptimized(const char *pattern, const char *text);
int  count_rk_optimized(const char *pattern, const char *text);
int  find_first_rk(const char *pattern, const char *text);
int  find_last_rk(const char *pattern, const char *text);

// --- KMP ---
int* prefix_function(const char *s, int n);
int* kmp_search(const char *pattern, const char *text, int *out_count);

// --- FFT + substring match via convolution ---
// (requires linking -lm and compile with -std=c99 -D_POSIX_C_SOURCE=200112L)
double* convolution(const double *a, const double *b, int n, int m, int *out_len);
int* fft_substring_match(const char *pattern, const char *text, int *out_count);

#endif // STRING_ALGORITHMS_H
